from textnode import TextNode, TextType
import re
from markdown_parser import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split TextNodes that are of type TEXT based on a delimiter and convert the content
    between delimiters to the specified text_type.

    Args:
        old_nodes: List of TextNode objects
        delimiter: String delimiter to split on (e.g., "**" for bold)
        text_type: TextType to apply to the content between delimiters

    Returns:
        A new list of TextNode objects with TEXT nodes potentially split
    """
    new_nodes = []

    for old_node in old_nodes:
        # If the node is not a TEXT type, add it as is and continue
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        # Get the text content
        text = old_node.text

        # Process text while there are still delimiters
        curr_index = 0
        while curr_index < len(text):
            # Find the next opening delimiter
            start_index = text.find(delimiter, curr_index)

            # If no opening delimiter is found, add the rest of the text and break
            if start_index == -1:
                if curr_index < len(text):
                    new_nodes.append(TextNode(text[curr_index:], TextType.TEXT))
                break

            # Add the text before the delimiter if there is any
            if start_index > curr_index:
                new_nodes.append(TextNode(text[curr_index:start_index], TextType.TEXT))

            # Find the closing delimiter
            end_index = text.find(delimiter, start_index + len(delimiter))

            # If no closing delimiter is found, raise an error
            if end_index == -1:
                raise ValueError(
                    f"Invalid markdown: Opening {delimiter} without closing {delimiter}"
                )

            # Extract the content between delimiters
            content = text[start_index + len(delimiter) : end_index]

            # Add the content with the specified text_type
            new_nodes.append(TextNode(content, text_type))

            # Move past the closing delimiter
            curr_index = end_index + len(delimiter)

    return new_nodes


def split_nodes_image(old_nodes):
    """
    Split TextNodes that are of type TEXT based on markdown image syntax ![alt](url).

    Args:
        old_nodes: List of TextNode objects

    Returns:
        A new list of TextNode objects with TEXT nodes potentially split
    """
    new_nodes = []

    for old_node in old_nodes:
        # If the node is not a TEXT type, add it as is and continue
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        # Get the text content
        text = old_node.text

        # Extract all images from the text
        images = extract_markdown_images(text)

        # If no images found, keep the node as is
        if not images:
            new_nodes.append(old_node)
            continue

        # Start processing text
        remaining_text = text

        # Process each image
        for alt_text, url in images:
            # Split the text at the image markdown
            image_markdown = f"![{alt_text}]({url})"
            parts = remaining_text.split(image_markdown, 1)

            # Add the text before the image if it's not empty
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            # Add the image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

            # Update remaining text
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""

        # Add any remaining text if it's not empty
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    """
    Split TextNodes that are of type TEXT based on markdown link syntax [anchor](url).

    Args:
        old_nodes: List of TextNode objects

    Returns:
        A new list of TextNode objects with TEXT nodes potentially split
    """
    new_nodes = []

    for old_node in old_nodes:
        # If the node is not a TEXT type, add it as is and continue
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        # Get the text content
        text = old_node.text

        # Extract all links from the text
        links = extract_markdown_links(text)

        # If no links found, keep the node as is
        if not links:
            new_nodes.append(old_node)
            continue

        # Start processing text
        remaining_text = text

        # Process each link
        for anchor_text, url in links:
            # Split the text at the link markdown
            link_markdown = f"[{anchor_text}]({url})"
            parts = remaining_text.split(link_markdown, 1)

            # Add the text before the link if it's not empty
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            # Add the link node
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))

            # Update remaining text
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""

        # Add any remaining text if it's not empty
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    """
    Convert a markdown text string into a list of TextNode objects.

    Args:
        text: A string of markdown-flavored text

    Returns:
        A list of TextNode objects
    """
    # Start with a single TextNode containing the entire text
    nodes = [TextNode(text, TextType.TEXT)]

    # Apply the splitting functions in sequence
    # First, handle images and links
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    # Then handle text styles
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes
