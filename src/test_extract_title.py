import unittest
from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_basic_title(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_title_with_whitespace(self):
        markdown = "#     Title with spaces    "
        self.assertEqual(extract_title(markdown), "Title with spaces")

    def test_title_with_other_content(self):
        markdown = """# My Page Title

This is some content.
## Subheading
More content here."""
        self.assertEqual(extract_title(markdown), "My Page Title")

    def test_no_title(self):
        markdown = """This is content without a title.
## This is a subheading, not a title
More content."""
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_multiple_titles(self):
        markdown = """# First Title
Content here.
# Second Title"""
        # Should return the first title found
        self.assertEqual(extract_title(markdown), "First Title")


if __name__ == "__main__":
    unittest.main()
