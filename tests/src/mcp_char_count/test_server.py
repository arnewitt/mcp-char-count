# tests/test_char_count.py
# Tests generated with ChatGPT

import pytest
import runpy
import logging
from server.src.mcp_char_count.server import (
    validate_input,
    char_count,
    get_character_count,
)

MODULE = "server.src.mcp_char_count.server"


@pytest.mark.parametrize(
    ("text", "char", "expected"),
    [("hello", "l", 2), ("", "a", 0), ("ßöä", "ö", 1)],
)
def test_char_count(text, char, expected):
    """Test the char_count function."""
    assert char_count(text, char) == expected


@pytest.mark.parametrize(
    ("text", "char"),
    [(123, "a"), ("abc", "ab"), ("a" * 10001, "a")],
)
def test_validate_input_raises(text, char):
    """Test the validate_input function for invalid inputs."""
    with pytest.raises(ValueError):
        validate_input(text, char)


@pytest.mark.asyncio
async def test_get_character_count_ok():
    """Test the get_character_count function with valid inputs."""
    assert await get_character_count("banana", "a") == 3


@pytest.mark.asyncio
async def test_get_character_count_invalid():
    """Test the get_character_count function with invalid inputs."""
    with pytest.raises(ValueError):
        await get_character_count("apple", "pp")


def test_main_success(monkeypatch):
    """Test the main function with a successful run method."""
    import sys

    sys.modules.pop(MODULE, None)

    called = {}

    def fake_run(self, **kw):
        called["kw"] = kw

    monkeypatch.setattr("mcp.server.fastmcp.FastMCP.run", fake_run, raising=True)

    monkeypatch.setattr(
        "sys.exit",
        lambda code=0: (_ for _ in ()).throw(
            AssertionError(f"sys.exit({code}) aufgerufen")
        ),
    )

    runpy.run_module(MODULE, run_name="__main__")

    assert called["kw"] == {"transport": "stdio"}


def test_main_failure(monkeypatch, caplog):
    """Test the main function with a failure in the run method."""

    def boom(self, **_):
        raise RuntimeError("boom")

    monkeypatch.setattr("mcp.server.fastmcp.FastMCP.run", boom, raising=True)

    exit_code = {}

    def fake_exit(code=0):
        """Fake sys.exit to capture the exit code."""
        exit_code["code"] = code
        raise SystemExit(code)

    monkeypatch.setattr("sys.exit", fake_exit)

    with caplog.at_level(logging.CRITICAL), pytest.raises(SystemExit):
        runpy.run_module(MODULE, run_name="__main__")

    assert exit_code["code"] == 1
    assert any(
        "Server encountered a fatal error" in r.getMessage() for r in caplog.records
    )
