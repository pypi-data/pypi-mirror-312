import sys
import click
import logging
from pathlib import Path
from .server import serve


@click.command()
@click.version_option()
@click.argument("vault_path", type=Path, required=False)
@click.option("--vault", "-r", type=Path, help="vault directory path")
@click.option("-v", "--verbose", count=True)
def main(vault_path: Path | None, vault: Path | None, verbose: bool):
    """MCP Obsidian Server"""
    import asyncio

    # vault_path 인자나 --vault 옵션 중 하나는 필수
    if vault_path is None and vault is None:
        raise click.UsageError("Vault directory path is required")

    # vault_path 인자가 우선
    vault_dir = vault_path or vault

    if not vault_dir.exists():
        raise click.UsageError(f"Vault directory does not exist: {vault_dir}")

    if not vault_dir.is_dir():
        raise click.UsageError(f"Vault path is not a directory: {vault_dir}")

    logging_level = logging.WARN
    if verbose == 1:
        logging_level = logging.INFO
    elif verbose >= 2:
        logging_level = logging.DEBUG

    logging.basicConfig(level=logging_level, stream=sys.stderr)
    asyncio.run(serve(vault_dir))


if __name__ == "__main__":
    main()
