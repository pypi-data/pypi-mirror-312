import sys
import click
import logging
from pathlib import Path
from .server import serve


@click.command()
@click.option("--vault", "-r", type=Path, help="vault directory path")
@click.option("-v", "--verbose", count=True)
def main(vault: Path | None, verbose: bool):
    """MCP Obsidian Server"""
    import asyncio

    if vault is None:
        raise click.UsageError("Vault directory path is required")
    
    if not vault.exists():
        raise click.UsageError(f"Vault directory does not exist: {vault}")
    
    if not vault.is_dir():
        raise click.UsageError(f"Vault path is not a directory: {vault}")

    logging_level = logging.WARN
    if verbose == 1:
        logging_level = logging.INFO
    elif verbose >= 2:
        logging_level = logging.DEBUG

    logging.basicConfig(level=logging_level, stream=sys.stderr)
    asyncio.run(serve([vault]))


if __name__ == "__main__":
    main()
