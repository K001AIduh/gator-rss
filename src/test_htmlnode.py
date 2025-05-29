import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_no_props(self):
        node = HTMLNode("p", "Hello, world!")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_one_prop(self):
        node = HTMLNode("a", "Click me!", props={"href": "https://www.boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(
            "a",
            "Click me!",
            props={
                "href": "https://www.boot.dev",
                "target": "_blank",
                "class": "btn btn-primary",
            },
        )
        # We need to check for the presence of each attribute since dictionary order is not guaranteed
        html_props = node.props_to_html()
        self.assertIn(' href="https://www.boot.dev"', html_props)
        self.assertIn(' target="_blank"', html_props)
        self.assertIn(' class="btn btn-primary"', html_props)

    def test_to_html_not_implemented(self):
        node = HTMLNode("p", "Hello, world!")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_init_optional_parameters(self):
        # Test that all parameters are optional
        node1 = HTMLNode()
        self.assertIsNone(node1.tag)
        self.assertIsNone(node1.value)
        self.assertIsNone(node1.children)
        self.assertIsNone(node1.props)

        # Test with only tag
        node2 = HTMLNode("div")
        self.assertEqual(node2.tag, "div")
        self.assertIsNone(node2.value)
        self.assertIsNone(node2.children)
        self.assertIsNone(node2.props)

        # Test with tag and value
        node3 = HTMLNode("p", "Hello")
        self.assertEqual(node3.tag, "p")
        self.assertEqual(node3.value, "Hello")
        self.assertIsNone(node3.children)
        self.assertIsNone(node3.props)


if __name__ == "__main__":
    unittest.main()
