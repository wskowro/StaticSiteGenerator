import unittest
from textnode import TextNode, TextType
from leafnode import LeafNode
from converter import *


class TestTextNodeToHtmlNode(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold")

    def test_italic(self):
        node = TextNode("Italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic")

    def test_code(self):
        node = TextNode("x = 1", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "x = 1")

    def test_link(self):
        node = TextNode("Google", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Google")
        self.assertEqual(html_node.props, {"href": "https://google.com"})

    def test_image(self):
        node = TextNode("An image", TextType.IMAGE,
                        "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {
            "src": "https://example.com/image.png",
            "alt": "An image"
        })

    def test_invalid_type(self):
        class FakeType:
            pass
        node = TextNode("oops", FakeType())
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_bold(self):
        node = TextNode("This has **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_italic(self):
        node = TextNode("This is _italic_ and _more_", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("more", TextType.ITALIC),
        ]
        self.assertEqual(result, expected)

    def test_no_delimiter(self):
        node = TextNode("No delimiters here", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [node]
        self.assertEqual(result, expected)

    def test_non_text_node_unchanged(self):
        node = TextNode("An image", TextType.IMAGE,
                        "https://example.com/image.png")
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])

    def test_multiple_nodes(self):
        nodes = [
            TextNode("Some _italic_ text", TextType.TEXT),
            TextNode("Bold **here** too", TextType.TEXT)
        ]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        result = split_nodes_delimiter(result, "**", TextType.BOLD)

        expected = [
            TextNode("Some ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
            TextNode("Bold ", TextType.TEXT),
            TextNode("here", TextType.BOLD),
            TextNode(" too", TextType.TEXT),
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
