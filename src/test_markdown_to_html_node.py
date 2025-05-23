import unittest
from extractmarkdown import *
from converter import *

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_heading_conversion(self):
        markdown = "# This is a heading"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.tag, 'div')
        self.assertEqual(node.children[0].tag, 'h1')
        self.assertEqual(node.children[0].children[0].value, 'This is a heading')

    def test_code_block_conversion(self):
        markdown = "```print('Hello')```"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.tag, 'div')
        code_node = node.children[0]
        self.assertEqual(code_node.tag, 'pre')
        self.assertEqual(code_node.children[0].tag, 'code')
        self.assertEqual(code_node.children[0].children[0].value, "print('Hello')")

if __name__ == '__main__':
    unittest.main()
