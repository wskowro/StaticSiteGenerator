from enum import Enum
import re

Blocktype = Enum("Blocktype", ["PARAGRAPH", "HEADING",
                 "CODE", "QUOTE", "UNORDERED_LIST", "ORDERED_LIST"])


def block_to_block_type(markdown):
    match markdown:
        case _ if re.match(r'^#{1,6} ', markdown):
            return Blocktype.HEADING
        case _ if re.match(r'^```.*```$', markdown):
            return Blocktype.CODE
        case _ if re.match(r'^>\s?', markdown):
            return Blocktype.QUOTE
        case _ if re.match(r'^-\s?', markdown):
            return Blocktype.UNORDERED_LIST
        case _ if re.match(r'^\d+\. ', markdown):
            return Blocktype.ORDERED_LIST
        case _:
            return Blocktype.PARAGRAPH
