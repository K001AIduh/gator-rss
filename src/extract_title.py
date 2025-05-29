def extract_title(markdown):
    """
    Extract the h1 header from markdown content.

    Args:
        markdown (str): The markdown content

    Returns:
        str: The extracted title (without # and whitespace)

    Raises:
        Exception: If no h1 header is found
    """
    lines = markdown.split("\n")

    for line in lines:
        if line.strip().startswith("# "):
            # Found h1 header, extract the title
            return line.strip()[2:].strip()

    # No h1 header found
    raise Exception("No h1 header found in markdown content")
