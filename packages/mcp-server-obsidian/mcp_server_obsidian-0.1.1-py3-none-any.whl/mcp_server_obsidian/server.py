#!/usr/bin/env python3

import asyncio
import logging
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, AsyncGenerator
from functools import partial

import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from pydantic import BaseModel


# 최대 검색 결과 수
SEARCH_LIMIT = 200


class SearchNotesScheme(BaseModel):
    query: str


class ReadNotesScheme(BaseModel):
    paths: List[str]


async def serve(vault_directories: List[Path]):
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger("mcp-server-obsidian")
    
    # Add file handler for persistent logging
    file_handler = logging.FileHandler('mcp_server.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(file_handler)

    if not vault_directories:
        logger.error("No vault directories provided")
        raise ValueError("No vault directories provided")

    logger.info(f"Starting server with vault directories: {vault_directories}")

    def normalize_path(p: Path) -> Path:
        """경로를 일관되게 정규화"""
        return Path(os.path.normpath(str(p))).resolve()

    def expand_home(filepath: str) -> Path:
        """~ 경로 확장"""
        if filepath.startswith("~/") or filepath == "~":
            expanded = os.path.expanduser("~")
            return Path(expanded) / (filepath[2:] if len(filepath) > 1 else "")
        return Path(filepath)

    async def validate_path(requested_path: str) -> Path:
        """경로 유효성 검사"""
        # 숨김 파일/디렉토리 무시
        path_parts = Path(requested_path).parts
        if any(part.startswith(".") for part in path_parts):
            raise ValueError("Access denied - hidden files/directories not allowed")

        expanded_path = expand_home(requested_path)
        normalized_requested = normalize_path(expanded_path)

        # 허용된 디렉토리 내에 있는지 확인
        is_allowed = any(
            str(normalized_requested).startswith(str(normalize_path(dir_)))
            for dir_ in vault_directories
        )
        if not is_allowed:
            raise ValueError(
                f"Access denied - path outside allowed directories: {normalized_requested} not in {', '.join(map(str, vault_directories))}"
            )

        return normalized_requested

    async def search_files(directory: Path, pattern: str) -> AsyncGenerator[Path, None]:
        """비동기적으로 파일 검색"""
        import aiohttp
        import urllib.parse
        import time

        start_time = time.time()
        logger.info(f"Starting search in {directory} with pattern: {pattern}")

        # HTTP 요청 시도
        try:
            encoded_query = urllib.parse.quote(pattern)
            async with aiohttp.ClientSession() as session:
                logger.debug(f"Attempting HTTP search with query: {encoded_query}")
                async with session.get(
                    f"http://localhost:51361/search?q={encoded_query}"
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"HTTP search successful, found {len(data)} results")
                        # score 순으로 정렬하고 path만 추출
                        sorted_results = sorted(
                            data, key=lambda x: x["score"], reverse=True
                        )
                        for result in sorted_results:
                            yield Path(result["path"])
                        
                        search_time = time.time() - start_time
                        logger.info(f"Search completed in {search_time:.2f} seconds")
                        return

        except Exception as e:
            logger.warning(f"HTTP request failed: {e}. Falling back to local search.", exc_info=True)

        # 기존 검색 로직 (HTTP 요청 실패시 실행)
        try:
            logger.info("Starting local file system search")
            entries = await asyncio.to_thread(os.scandir, str(directory))

            for entry in entries:
                try:
                    entry_path = Path(entry.path)

                    # 경로 검증
                    try:
                        await validate_path(str(entry_path))
                    except ValueError:
                        continue

                    # 파일 이름 매칭 검사
                    name = entry.name.lower()
                    query = pattern.lower()

                    matches = query in name
                    try:
                        matches = matches or bool(
                            re.search(query.replace("*", ".*"), name, re.I)
                        )
                    except re.error:
                        pass

                    if entry.is_file() and entry.name.endswith(".md") and matches:
                        yield entry_path

                    # 디렉토리인 경우 재귀적으로 검색
                    if entry.is_dir():
                        async for found in search_files(entry_path, pattern):
                            yield found

                except (PermissionError, OSError) as e:
                    logger.warning(f"Error accessing {entry.path}: {e}")
                    continue

        except (PermissionError, OSError) as e:
            logger.error(f"Error scanning directory {directory}: {e}")

    async def search_notes(query: str) -> List[str]:
        """노트 검색"""
        logger.info(f"Searching notes with query: {query}")
        start_time = time.time()
        
        results = []
        count = 0

        for vault_dir in vault_directories:
            logger.debug(f"Searching in vault directory: {vault_dir}")
            async for file_path in search_files(vault_dir, query):
                if count >= SEARCH_LIMIT:
                    logger.info(f"Search limit ({SEARCH_LIMIT}) reached")
                    break

                try:
                    relative_path = str(file_path.relative_to(vault_dir))
                    results.append(relative_path)
                    count += 1
                except ValueError as e:
                    logger.warning(f"Failed to get relative path for {file_path}: {e}")
                    continue

        search_time = time.time() - start_time
        logger.info(f"Search completed in {search_time:.2f} seconds, found {len(results)} results")
        return results

    app = Server("mcp-server-obsidian")

    # 도구 목록 정의
    tools = [
        types.Tool(
            name="read_notes",
            description=(
                "Read the contents of multiple notes. Each note's content is returned with its "
                "path as a reference. Failed reads for individual notes won't stop "
                "the entire operation. Reading too many at once may result in an error."
            ),
            inputSchema=ReadNotesScheme.schema(),
        ),
        types.Tool(
            name="search_notes",
            description=(
                "Searches for a note by its name. The search "
                "is case-insensitive and matches partial names. "
                "Queries can also be a valid regex. Returns paths of the notes "
                "that match the query."
            ),
            inputSchema=SearchNotesScheme.schema(),
        ),
    ]

    @app.list_tools
    async def list_tools():
        """사용 가능한 도구 목록 반환"""
        return tools

    @app.call_tool
    async def call_tool(
        tool: types.Tool, arguments: Dict[str, Any]
    ) -> List[types.TextContent]:
        """도구 호출 처리"""
        logger.info(f"Tool call received: {tool.name}")
        logger.debug(f"Tool arguments: {arguments}")
        
        try:
            if tool.name == "read_notes":
                if not isinstance(arguments, dict) or "paths" not in arguments:
                    logger.error("Invalid arguments for read_notes")
                    raise ValueError("Invalid arguments for read_notes")

                results = []
                for file_path in arguments["paths"]:
                    try:
                        logger.debug(f"Reading note: {file_path}")
                        valid_path = await validate_path(
                            os.path.join(str(vault_directories[0]), file_path)
                        )
                        content = (
                            await asyncio.to_thread(
                                partial(open, valid_path, "r", encoding="utf-8")
                            )
                            .__aenter__()
                            .read()
                        )
                        results.append(f"{file_path}:<br>{content}<br>")
                        logger.debug(f"Successfully read note: {file_path}")
                    except Exception as e:
                        logger.error(f"Error reading {file_path}: {e}", exc_info=True)
                        results.append(f"{file_path}: Error - {str(e)}")

                logger.info(f"Completed reading {len(results)} notes")
                return [
                    types.TextContent(type="text", text="<br>---<br>".join(results))
                ]

            elif tool.name == "search_notes":
                if not isinstance(arguments, dict) or "query" not in arguments:
                    logger.error("Invalid arguments for search_notes")
                    raise ValueError("Invalid arguments for search_notes")

                results = await search_notes(arguments["query"])
                limited_results = results[:SEARCH_LIMIT]

                text = (
                    "<br>".join(limited_results)
                    if limited_results
                    else "No matches found"
                )
                if len(results) > SEARCH_LIMIT:
                    text += f"<br><br>... {len(results) - SEARCH_LIMIT} more results not shown."
                
                logger.info(f"Search completed, found {len(results)} results (showing {len(limited_results)})")
                return [types.TextContent(type="text", text=text)]

            else:
                logger.error(f"Unknown tool: {tool.name}")
                raise ValueError(f"Unknown tool: {tool.name}")

        except Exception as e:
            logger.error(f"Error in call_tool: {e}", exc_info=True)
            raise

    logger.info("Server initialization completed")
    return app


def main():
    """메인 함수"""
    import argparse

    parser = argparse.ArgumentParser(description="Obsidian vault MCP server")
    parser.add_argument(
        "vault_directories",
        nargs="+",
        type=str,
        help="Path to Obsidian vault directories",
    )
    args = parser.parse_args()

    vault_paths = [Path(path) for path in args.vault_directories]
    asyncio.run(stdio_server(serve(vault_paths)))


if __name__ == "__main__":
    main()
