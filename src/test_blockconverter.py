import unittest
from textnode import TextNode, TextType
from leafnode import LeafNode
from converter import *


class TestMarkdownToBlockConversion(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_paragraph(self):
        md = "This is a single paragraph."
        expected = ["This is a single paragraph."]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_multiple_paragraphs(self):
        md = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
        expected = ["First paragraph.", "Second paragraph.", "Third paragraph."]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_leading_trailing_whitespace(self):
        md = "   First paragraph.   \n\n   Second paragraph.   "
        expected = ["First paragraph.", "Second paragraph."]
        self.assertEqual(markdown_to_blocks(md), expected)

if __name__ == "__main__":
    unittest.main()
