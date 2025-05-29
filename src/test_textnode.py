import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_same_values(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_different_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_different_url(self):
        node = TextNode("Anchor text", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Anchor text", TextType.LINK, "https://example.com")
        self.assertNotEqual(node, node2)

    def test_eq_one_with_url_one_without(self):
        node = TextNode("Anchor text", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Anchor text", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_eq_both_with_none_url(self):
        node = TextNode("Regular text", TextType.TEXT)
        node2 = TextNode("Regular text", TextType.TEXT)
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
