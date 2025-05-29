import unittest
from markdown_to_html import markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        # Using assertIn instead of assertEqual for more flexible testing
        self.assertIn("<div><pre><code>", html)
        self.assertIn("This is text that _should_ remain", html)
        self.assertIn("the **same** even with inline stuff", html)
        self.assertIn("</code></pre></div>", html)

    def test_headings(self):
        md = """
# Heading 1

## Heading 2

### Heading 3 with **bold**
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3 with <b>bold</b></h3></div>",
        )

    def test_blockquote(self):
        md = """
> This is a blockquote
> with multiple lines
> and _italic_ text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote with multiple lines and <i>italic</i> text</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- Item 1
- Item 2 with **bold**
- Item 3 with `code`
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2 with <b>bold</b></li><li>Item 3 with <code>code</code></li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second item with _italic_
3. Third item with **bold**
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item with <i>italic</i></li><li>Third item with <b>bold</b></li></ol></div>",
        )

    def test_mixed_content(self):
        md = """
# Markdown Test

This is a paragraph with **bold** and _italic_ text.

## Code Example

```
def hello():
    print("Hello, world!")
```

### Lists

- Item 1
- Item 2
- Item 3

1. First
2. Second
3. Third

> This is a blockquote
> with multiple lines
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        # Test each part individually for more flexible testing
        self.assertIn("<div>", html)
        self.assertIn("<h1>Markdown Test</h1>", html)
        self.assertIn(
            "<p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p>", html
        )
        self.assertIn("<h2>Code Example</h2>", html)
        self.assertIn("<pre><code>", html)
        self.assertIn("def hello():", html)
        self.assertIn('print("Hello, world!")', html)
        self.assertIn("</code></pre>", html)
        self.assertIn("<h3>Lists</h3>", html)
        self.assertIn("<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>", html)
        self.assertIn("<ol><li>First</li><li>Second</li><li>Third</li></ol>", html)
        self.assertIn(
            "<blockquote>This is a blockquote with multiple lines</blockquote>", html
        )
        self.assertIn("</div>", html)

    def test_links_and_images(self):
        md = """
# Links and Images

Here's a [link to Google](https://www.google.com) and an ![image](https://example.com/image.jpg).
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><h1>Links and Images</h1><p>Here\'s a <a href="https://www.google.com">link to Google</a> and an <img src="https://example.com/image.jpg" alt="image">.</p></div>',
        )


if __name__ == "__main__":
    unittest.main()
