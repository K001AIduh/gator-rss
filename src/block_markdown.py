from enum import Enum, auto


class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()


def markdown_to_blocks(markdown):
    """
    Split a markdown string into blocks based on blank lines.

    Args:
        markdown: A string containing markdown text

    Returns:
        A list of strings where each string is a markdown block
    """
    # Strip leading and trailing whitespace from the entire document
    markdown = markdown.strip()

    # Split the document on double newlines
    blocks = markdown.split("\n\n")

    # Clean up each block
    cleaned_blocks = []
    for block in blocks:
        # Strip leading and trailing whitespace from the block
        block = block.strip()

        # Only add non-empty blocks
        if block:
            cleaned_blocks.append(block)

    return cleaned_blocks


def block_to_block_type(block):
    """
    Determine the type of a markdown block.

    Args:
        block: A string containing a markdown block

    Returns:
        A BlockType representing the type of block
    """
    # Check if it's a code block
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Split block into lines for analyzing line-by-line patterns
    lines = block.split("\n")

    # Check if it's a heading
    if lines[0].startswith("#"):
        # Ensure it has a space after the # (standard markdown)
        hash_count = 0
        for char in lines[0]:
            if char == "#":
                hash_count += 1
            else:
                break

        if 1 <= hash_count <= 6 and lines[0][hash_count : hash_count + 1] == " ":
            return BlockType.HEADING

    # Check if it's a quote block (all lines must start with >)
    all_quote_lines = all(line.startswith(">") for line in lines)
    if all_quote_lines:
        return BlockType.QUOTE

    # Check if it's an unordered list (all lines must start with -)
    all_unordered_list_lines = all(line.startswith("- ") for line in lines)
    if all_unordered_list_lines:
        return BlockType.UNORDERED_LIST

    # Check if it's an ordered list
    if all(len(line) >= 3 for line in lines):  # Each line must be at least "1. "
        # Check if each line starts with a number followed by a period and a space
        is_ordered_list = True
        expected_number = 1

        for line in lines:
            # Find the position of the first period
            period_pos = line.find(".")
            if period_pos == -1:
                is_ordered_list = False
                break

            # Extract the part before the period
            prefix = line[:period_pos]

            # Check if the prefix is a number and matches the expected number
            if not prefix.isdigit() or int(prefix) != expected_number:
                is_ordered_list = False
                break

            # Check if the period is followed by a space
            if len(line) <= period_pos + 1 or line[period_pos + 1] != " ":
                is_ordered_list = False
                break

            expected_number += 1

        if is_ordered_list:
            return BlockType.ORDERED_LIST

    # If none of the above, it's a paragraph
    return BlockType.PARAGRAPH
