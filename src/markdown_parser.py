import re


def extract_markdown_images(text):
    """
    Extract all markdown images from text.

    Args:
        text: The markdown text to parse

    Returns:
        A list of tuples where each tuple contains (alt_text, url)
    """
    # Pattern: ![alt text](url)
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    """
    Extract all markdown links from text.

    Args:
        text: The markdown text to parse

    Returns:
        A list of tuples where each tuple contains (anchor_text, url)
    """
    # Pattern: [anchor text](url) but not preceded by an exclamation mark
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches
