# MCP Server Obsidian

A Model Context Protocol server that provides Obsidian vault search capabilities. This server enables LLMs to search and retrieve content from your Obsidian vault, making it easier to find and process your notes.

### Available Tools

- `search` - Searches your Obsidian vault for notes matching the query.
    - `query` (string, required): Search query to find relevant notes
    - Returns a list of matching notes with their content

### Features

- Search through your entire Obsidian vault
- Secure access with path validation
- Configurable search limits
- Hidden files/directories are automatically ignored

## Installation

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *mcp-server-obsidian*.

### Using PIP

Alternatively you can install `mcp-server-obsidian` via pip:

```
pip install mcp-server-obsidian
```

After installation, you can run it as a script using:

```
python -m mcp_server_obsidian
```

## Configuration

The server needs to be configured with your Obsidian vault directory. By default, it will look for notes in the user's home directory.

### Security

The server includes several security features:
- Path validation to prevent unauthorized access
- Hidden files and directories are automatically ignored
- Access is restricted to configured vault directories only

## Development

To contribute to this project:

1. Clone the repository
2. Install dependencies
3. Run the server using `python -m mcp_server_obsidian`

## License

This project is licensed under the MIT License - see the LICENSE file for details.
