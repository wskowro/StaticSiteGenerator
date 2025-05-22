import unittest
from textnode import TextNode, TextType
from converter import *


class TestSplitNodes(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE,
                         "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "Check [Google](https://google.com) and [GitHub](https://github.com).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "https://google.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("GitHub", TextType.LINK, "https://github.com"),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_no_images(self):
        node = TextNode("No images here.", TextType.TEXT)
        self.assertListEqual(split_nodes_image([node]), [node])

    def test_no_links(self):
        node = TextNode("No links here.", TextType.TEXT)
        self.assertListEqual(split_nodes_link([node]), [node])

    def test_mixed_nodes(self):
        nodes = [
            TextNode("Some text ", TextType.TEXT),
            TextNode("not touched", TextType.BOLD),
            TextNode(
                " with an ![image](https://example.com/image.png)", TextType.TEXT),
        ]
        expected = [
            TextNode("Some text ", TextType.TEXT),
            TextNode("not touched", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
        ]
        self.assertListEqual(split_nodes_image(nodes), expected)


if __name__ == "__main__":
    unittest.main()
