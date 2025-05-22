import unittest
from textnode import TextNode, TextType
from converter import *


class TestTextToTextNodes(unittest.TestCase):
    def test_full_example(self):
        input_text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE,
                     "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        actual = text_to_textnodes(input_text)
        self.assertListEqual(expected, actual)

    def test_only_text(self):
        input_text = "Just plain text here."
        expected = [TextNode("Just plain text here.", TextType.TEXT)]
        self.assertListEqual(text_to_textnodes(input_text), expected)


def test_nested_formatting(self):
    input_text = "Mix **bold _italic_** and `code`"
    expected = [
        TextNode("Mix ", TextType.TEXT),
        TextNode("bold _italic_", TextType.BOLD),
        TextNode(" and ", TextType.TEXT),
        TextNode("code", TextType.CODE),
    ]
    self.assertListEqual(text_to_textnodes(input_text), expected)


if __name__ == "__main__":
    unittest.main()
