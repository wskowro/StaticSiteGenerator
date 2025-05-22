import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_props_to_html_basic(self):
        node = LeafNode("p", "Hello, world!",
                        props={"href": "https://www.google.com", "target": "_blank"})
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_empty(self):
        node = LeafNode("p", "Hello, balloons")
        expected = ""
        self.assertEqual(node.props_to_html(), expected)

    def test_repr_contains_expected_values(self):
        node = LeafNode(tag="a", value="Click me", props={
                        "href": "https://example.com"})
        representation = repr(node)
        self.assertIn("Click me", representation)
        self.assertIn("href", representation)
        self.assertIn("example.com", representation)


if __name__ == "__main__":
    unittest.main()
