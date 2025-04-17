# mcp-char-count
Model context protocol (MCP) server to count character occurrences in strings.

## Setup

For the setup with Claude Desktop, go [here](server/src/mcp_char_count/README.md).

## Testing

Test the code with pytest:

```bash
uv run -m pytest --cov=server --cov-report=term-missing
```