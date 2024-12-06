import os
import pytest
import asyncio
from pathlib import Path
from unittest.mock import patch, mock_open, AsyncMock

from mcp_server_obsidian.server import serve, SearchNotesScheme, ReadNotesScheme
from mcp.types import TextContent, Tool

@pytest.fixture
def test_vault_dir(tmp_path):
    """테스트용 임시 vault 디렉토리 생성"""
    # 테스트 노트 파일 생성
    note1 = tmp_path / "test_note1.md"
    note1.write_text("Test content 1")
    note2 = tmp_path / "test_note2.md"
    note2.write_text("Test content 2")
    return tmp_path

@pytest.mark.asyncio
async def test_search_notes():
    """노트 검색 기능 테스트"""
    test_dir = Path("/test/vault")
    with patch("os.scandir") as mock_scandir:
        # Mock scandir 결과 설정
        mock_entry1 = type("MockEntry", (), {
            "name": "test_note1.md",
            "path": str(test_dir / "test_note1.md"),
            "is_file": lambda: True,
            "is_dir": lambda: False
        })
        mock_entry2 = type("MockEntry", (), {
            "name": "test_note2.md",
            "path": str(test_dir / "test_note2.md"),
            "is_file": lambda: True,
            "is_dir": lambda: False
        })
        mock_scandir.return_value = [mock_entry1, mock_entry2]

        # 서버 초기화
        app = await serve([test_dir])
        
        # 도구 목록 가져오기
        tools = await app.list_tools()
        search_tool = next(t for t in tools if t.name == "search_notes")
        
        # search_notes 도구 호출
        result = await app.call_tool(search_tool, {"query": "test"})
        
        # 결과 검증
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        assert "test_note1.md" in result[0].text
        assert "test_note2.md" in result[0].text

@pytest.mark.asyncio
async def test_read_notes():
    """노트 읽기 기능 테스트"""
    test_dir = Path("/test/vault")
    test_content = "Test note content"
    
    with patch("builtins.open", mock_open(read_data=test_content)):
        # 서버 초기화
        app = await serve([test_dir])
        
        # 도구 목록 가져오기
        tools = await app.list_tools()
        read_tool = next(t for t in tools if t.name == "read_notes")
        
        # read_notes 도구 호출
        result = await app.call_tool(read_tool, {"paths": ["test_note1.md"]})
        
        # 결과 검증
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        assert test_content in result[0].text

@pytest.mark.asyncio
async def test_invalid_path():
    """잘못된 경로 처리 테스트"""
    test_dir = Path("/test/vault")
    
    # 서버 초기화
    app = await serve([test_dir])
    
    # 도구 목록 가져오기
    tools = await app.list_tools()
    read_tool = next(t for t in tools if t.name == "read_notes")
    
    # 숨김 파일 접근 시도
    with pytest.raises(ValueError, match="Access denied - hidden files/directories not allowed"):
        await app.call_tool(read_tool, {"paths": [".hidden_note.md"]})
    
    # 허용되지 않은 디렉토리 접근 시도
    with pytest.raises(ValueError, match="Access denied - path outside allowed directories"):
        await app.call_tool(read_tool, {"paths": ["/unauthorized/path/note.md"]})

@pytest.mark.asyncio
async def test_search_limit():
    """검색 결과 제한 테스트"""
    test_dir = Path("/test/vault")
    with patch("os.scandir") as mock_scandir:
        # 많은 수의 mock 파일 생성
        mock_entries = []
        for i in range(250):  # SEARCH_LIMIT(200)보다 많은 파일
            mock_entry = type("MockEntry", (), {
                "name": f"test_note{i}.md",
                "path": str(test_dir / f"test_note{i}.md"),
                "is_file": lambda: True,
                "is_dir": lambda: False
            })
            mock_entries.append(mock_entry)
        mock_scandir.return_value = mock_entries

        # 서버 초기화
        app = await serve([test_dir])
        
        # 도구 목록 가져오기
        tools = await app.list_tools()
        search_tool = next(t for t in tools if t.name == "search_notes")
        
        # search_notes 도구 호출
        result = await app.call_tool(search_tool, {"query": "test"})
        
        # 결과가 SEARCH_LIMIT(200)을 초과하지 않는지 확인
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        text_lines = result[0].text.split("<br>")
        assert len([line for line in text_lines if line and not line.startswith("...")]) <= 200
        assert "more results not shown" in result[0].text
