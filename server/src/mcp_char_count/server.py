import logging
import sys
from typing import Any
from mcp.server.fastmcp import FastMCP

# Setup structured logging
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize server
mcp = FastMCP(name="char-count")


def validate_input(text: str, char: str) -> None:
    """
    Validate inputs to ensure secure and proper behavior.
    Raises ValueError if any input does not meet the criteria.

    Args:
        text (str): The input string.
        char (str): The character to count.

    Raises:
        ValueError: If the input text is not a string or the character is not a single character.
    """
    if not isinstance(text, str):
        raise ValueError("Input text must be a string.")
    if not isinstance(char, str) or len(char) != 1:
        raise ValueError("Input char must be a single character.")
    if (
        len(text) > 10000
    ):  # Limit input size to avoid abuse (adjust threshold as needed)
        raise ValueError("Input text exceeds maximum allowed length.")


# Define helper function
def char_count(text: str, char: str) -> int:
    """
    Counts the occurrences of a specific character in a given string.

    Args:
        text (str): The string in which to count occurrences of the character.
        char (str): The character to count within the string.

    Returns:
        int: The number of times the specified character appears in the string.

    Raises:
        ValueError: If `char` is not a single character.
    """
    return text.count(char)


@mcp.tool()
async def get_character_count(text: str, char: str) -> int:
    """
    Count occurrences of a character in a string.

    Args:
        text (str): The input string.
        char (str): The character to count.

    Returns:
        int: The count of occurrences of the character in the string.

    Raises:
        ValueError: If the input text is not a string or the character is not a single character.
        Exception: For any other unexpected errors.
    """
    try:
        validate_input(text, char)
        result = char_count(text, char)
        logger.info("Counted '%s' in text. Result: %d", char, result)
        return result
    except Exception as e:
        logger.error("Error in get_character_count: %s", e)
        raise


if __name__ == "__main__":
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        logger.critical("Server encountered a fatal error: %s", e)
        sys.exit(1)
