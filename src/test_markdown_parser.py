import unittest

from markdown_parser import extract_markdown_images, extract_markdown_links


class TestMarkdownParser(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("This is text with no images")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_with_links(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://example.com)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("This is text with no links")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_with_images(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_markdown_links_complex_url(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com/path?query=value&param=123#fragment)"
        )
        self.assertListEqual(
            [("link", "https://example.com/path?query=value&param=123#fragment")],
            matches,
        )

    def test_extract_markdown_images_complex_url(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png?width=100&height=200)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png?width=100&height=200")], matches
        )

    def test_extract_markdown_links_with_spaces(self):
        matches = extract_markdown_links(
            "This is text with a [link with spaces](https://example.com)"
        )
        self.assertListEqual([("link with spaces", "https://example.com")], matches)

    def test_extract_markdown_images_with_spaces(self):
        matches = extract_markdown_images(
            "This is text with an ![image with spaces](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image with spaces", "https://i.imgur.com/zjjcJKZ.png")], matches
        )


if __name__ == "__main__":
    unittest.main()
