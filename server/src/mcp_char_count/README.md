
# MCP Character Count Server

A simple microservice that counts the occurrences of a specific character within a given string.

## Features

*   Counts how often a specified character appears in a provided text.
*   Validates input securely.
*   Structured logging for debugging and monitoring.

## Claude desktop config
Add this to your `claude_desktop_config.json`:

```json
{
    "mcpServers": {
        "char-count": {
            "command": "uv",
            "args": [
                "--directory",
                "/abs/path/to/project/mcp-char-count/server/src/mcp_char_count",
                "run",
                "server.py"
            ]
        }
    }
}
```

## Input Validation

*   `text`: Must be a string up to 10,000 characters.
*   `char`: Must be exactly one character (string length = 1).
