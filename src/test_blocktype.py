import unittest
from blocktype import *

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), Blocktype.HEADING)
        self.assertEqual(block_to_block_type("###### Six"), Blocktype.HEADING)

    def test_code(self):
        self.assertEqual(block_to_block_type("```code block```"), Blocktype.CODE)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> A quote"), Blocktype.QUOTE)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- Item"), Blocktype.UNORDERED_LIST)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First"), Blocktype.ORDERED_LIST)
        self.assertEqual(block_to_block_type("42. Answer"), Blocktype.ORDERED_LIST)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("Just a normal paragraph."), Blocktype.PARAGRAPH)

if __name__ == '__main__':
    unittest.main()
