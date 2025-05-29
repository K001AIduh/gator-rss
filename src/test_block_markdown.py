import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_single_block(self):
        md = "Just one block with no blank lines"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just one block with no blank lines"])

    def test_multiple_empty_lines(self):
        md = """
First block


Second block with multiple empty lines in between
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block",
                "Second block with multiple empty lines in between",
            ],
        )

    def test_leading_trailing_whitespace(self):
        md = """

    Block with leading and trailing spaces

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block with leading and trailing spaces"])

    def test_code_blocks(self):
        md = """
Regular paragraph

```
Code block
with multiple lines
```

Another paragraph
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Regular paragraph",
                "```\nCode block\nwith multiple lines\n```",
                "Another paragraph",
            ],
        )

    def test_headers_and_lists(self):
        md = """
# Heading 1

## Heading 2

- List item 1
- List item 2

1. Numbered list
2. Second item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading 1",
                "## Heading 2",
                "- List item 1\n- List item 2",
                "1. Numbered list\n2. Second item",
            ],
        )

    def test_excessive_newlines(self):
        md = """
First block



Second block



Third block
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block",
                "Second block",
                "Third block",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a normal paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        block = "This paragraph has **bold** and _italic_ text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        block = "Paragraph with\nmultiple lines\nbut no special formatting."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = "## Heading 2"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = "###### Heading 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        # Not a heading - no space after #
        block = "#NoSpace"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # Not a heading - too many #
        block = "####### Too many hashes"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # Heading with multiple lines
        block = "# Heading\nWith multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code(self):
        block = "```\nCode block\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        block = "```python\ndef hello():\n    print('Hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        # Not a code block - missing ending backticks
        block = "```\nIncomplete code block"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # Not a code block - missing starting backticks
        block = "Incomplete code block\n```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        block = "> Quote with\n> multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        # Not a quote - not all lines start with >
        block = "> Quote start\nNot a quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block = "- List item 1"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

        block = "- List item 1\n- List item 2\n- List item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

        # Not an unordered list - not all lines start with -
        block = "- List item 1\nNot a list item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # Not an unordered list - missing space after -
        block = "-No space"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. List item 1"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

        block = "1. List item 1\n2. List item 2\n3. List item 3"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

        # Not an ordered list - not sequential
        block = "1. List item 1\n3. List item 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # Not an ordered list - not all lines start with a number
        block = "1. List item 1\nNot a list item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # Not an ordered list - missing space after period
        block = "1.No space"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # Not an ordered list - doesn't start with 1
        block = "2. Starts with 2\n3. Then 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
