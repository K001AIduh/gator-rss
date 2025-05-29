from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode, text_node_to_html_node
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType
from inline_markdown import text_to_textnodes


def text_to_children(text):
    """
    Convert a string of markdown text to a list of HTMLNode objects.

    Args:
        text: A string containing markdown text

    Returns:
        A list of HTMLNode objects
    """
    # Convert text to TextNode objects
    text_nodes = text_to_textnodes(text)

    # Convert TextNode objects to HTMLNode objects
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))

    return html_nodes


def heading_block_to_html_node(block):
    """
    Convert a heading block to an HTMLNode.

    Args:
        block: A string containing a heading block

    Returns:
        An HTMLNode representing the heading
    """
    # Count the number of # characters
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break

    # Extract the heading text
    text = block[level:].strip()

    # Convert the text to children nodes
    children = text_to_children(text)

    # Create and return a parent node with the appropriate heading tag
    return ParentNode(f"h{level}", children)


def paragraph_block_to_html_node(block):
    """
    Convert a paragraph block to an HTMLNode.

    Args:
        block: A string containing a paragraph block

    Returns:
        An HTMLNode representing the paragraph
    """
    # Replace newlines with spaces to create a single continuous paragraph
    block = block.replace("\n", " ")

    # Convert the text to children nodes
    children = text_to_children(block)

    # Create and return a parent node with a p tag
    return ParentNode("p", children)


def code_block_to_html_node(block):
    """
    Convert a code block to an HTMLNode.

    Args:
        block: A string containing a code block

    Returns:
        An HTMLNode representing the code block
    """
    # Extract code content (removing the triple backticks)
    lines = block.split("\n")

    if len(lines) >= 2 and lines[0].strip() == "```" and lines[-1].strip() == "```":
        # Multi-line code block with backticks on their own lines
        code_content = "\n".join(lines[1:-1])
    elif len(lines) >= 2 and lines[0].startswith("```") and lines[-1].endswith("```"):
        # Multi-line code block with backticks as part of the first/last lines
        first_line = lines[0][3:].strip()  # Remove the starting ```
        last_line = lines[-1][:-3].strip()  # Remove the ending ```

        middle_lines = lines[1:-1]
        if first_line:
            middle_lines.insert(0, first_line)
        if last_line:
            middle_lines.append(last_line)

        code_content = "\n".join(middle_lines)
    else:
        # Single line or invalid code block, just remove the backticks
        code_content = block.replace("```", "").strip()

    # Create a TextNode for the code content
    text_node = TextNode(code_content, TextType.TEXT)

    # Convert to an HTMLNode
    code_node = text_node_to_html_node(text_node)

    # Wrap in a code tag
    code_parent = ParentNode("code", [code_node])

    # Wrap in a pre tag
    return ParentNode("pre", [code_parent])


def quote_block_to_html_node(block):
    """
    Convert a quote block to an HTMLNode.

    Args:
        block: A string containing a quote block

    Returns:
        An HTMLNode representing the quote block
    """
    # Remove the > prefix from each line and join with spaces
    lines = block.split("\n")
    clean_lines = []
    for line in lines:
        if line.startswith(">"):
            # Remove the > and any leading space
            clean_lines.append(line[1:].lstrip())
        else:
            clean_lines.append(line)

    # Join the lines with spaces to create a continuous paragraph
    text = " ".join(clean_lines)

    # Convert the text to children nodes
    children = text_to_children(text)

    # Create and return a parent node with a blockquote tag
    return ParentNode("blockquote", children)


def unordered_list_block_to_html_node(block):
    """
    Convert an unordered list block to an HTMLNode.

    Args:
        block: A string containing an unordered list block

    Returns:
        An HTMLNode representing the unordered list
    """
    # Split the block into list items
    lines = block.split("\n")

    # Create list item nodes
    list_items = []
    for line in lines:
        # Remove the "- " prefix
        item_text = line[2:].strip()

        # Convert the text to children nodes
        children = text_to_children(item_text)

        # Create a list item node
        list_item = ParentNode("li", children)
        list_items.append(list_item)

    # Create and return a parent node with a ul tag
    return ParentNode("ul", list_items)


def ordered_list_block_to_html_node(block):
    """
    Convert an ordered list block to an HTMLNode.

    Args:
        block: A string containing an ordered list block

    Returns:
        An HTMLNode representing the ordered list
    """
    # Split the block into list items
    lines = block.split("\n")

    # Create list item nodes
    list_items = []
    for line in lines:
        # Find the position of the period
        period_pos = line.find(".")

        # Extract the item text (after the period and space)
        item_text = line[period_pos + 2 :].strip()

        # Convert the text to children nodes
        children = text_to_children(item_text)

        # Create a list item node
        list_item = ParentNode("li", children)
        list_items.append(list_item)

    # Create and return a parent node with an ol tag
    return ParentNode("ol", list_items)


def block_to_html_node(block):
    """
    Convert a markdown block to an HTMLNode.

    Args:
        block: A string containing a markdown block

    Returns:
        An HTMLNode representing the block
    """
    # Determine the block type
    block_type = block_to_block_type(block)

    # Convert the block to an HTMLNode based on its type
    if block_type == BlockType.PARAGRAPH:
        return paragraph_block_to_html_node(block)
    elif block_type == BlockType.HEADING:
        return heading_block_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_block_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_block_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return unordered_list_block_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return ordered_list_block_to_html_node(block)
    else:
        raise ValueError(f"Unknown block type: {block_type}")


def markdown_to_html_node(markdown):
    """
    Convert a markdown string to an HTMLNode.

    Args:
        markdown: A string containing markdown text

    Returns:
        An HTMLNode representing the entire markdown document
    """
    # Split the markdown into blocks
    blocks = markdown_to_blocks(markdown)

    # Convert each block to an HTMLNode
    html_nodes = []
    for block in blocks:
        html_nodes.append(block_to_html_node(block))

    # Create a parent div to hold all the blocks
    return ParentNode("div", html_nodes)
