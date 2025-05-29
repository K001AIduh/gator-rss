import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_href(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev">Click me!</a>')

    def test_leaf_to_html_multiple_props(self):
        node = LeafNode(
            "a",
            "Boot.dev",
            {"href": "https://www.boot.dev", "target": "_blank", "class": "link"},
        )
        html = node.to_html()
        self.assertTrue(html.startswith("<a "))
        self.assertTrue(html.endswith(">Boot.dev</a>"))
        self.assertIn(' href="https://www.boot.dev"', html)
        self.assertIn(' target="_blank"', html)
        self.assertIn(' class="link"', html)

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Raw text")
        self.assertEqual(node.to_html(), "Raw text")

    def test_leaf_to_html_no_value_raises_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_node_inherits_from_htmlnode(self):
        node = LeafNode("div", "Content")
        self.assertEqual(node.props_to_html(), "")

        node = LeafNode("div", "Content", {"class": "container"})
        self.assertEqual(node.props_to_html(), ' class="container"')


if __name__ == "__main__":
    unittest.main()
