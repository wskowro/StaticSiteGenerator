from textnode import TextNode, TextType
from leafnode import LeafNode
from htmlnode import *
from extractmarkdown import *
from blocktype import *
from parentnode import *
import re


def text_node_to_html_node(text_node):

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Unsupported TextType: {text_node.text_type}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        # If no delimiter found, parts will be just one item
        if len(parts) < 3 or len(parts) % 2 == 0:
            # If not an odd number of parts, treat as plain text
            new_nodes.append(node)
            continue

        for i, part in enumerate(parts):
            if not part:
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    pattern = r"!\[([^\]]+)\]\(([^)]+)\)"  # Matches ![alt](url)

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        while re.search(pattern, text):
            match = re.search(pattern, text)
            before = text[:match.start()]
            alt_text = match.group(1)
            url = match.group(2)
            text = text[match.end():]

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    pattern = r"\[([^\]]+)\]\(([^)]+)\)"  # Matches [text](url)

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        while re.search(pattern, text):
            match = re.search(pattern, text)
            before = text[:match.start()]
            link_text = match.group(1)
            url = match.group(2)
            text = text[match.end():]

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, url))

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(
        nodes, "`", TextType.CODE)  # This must be here
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    blocks = []
    for block in markdown.split("\n\n"):
        stripped_block = block.strip()
        blocks.append(stripped_block)
    return blocks


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == Blocktype.HEADING:
            level = len(re.match(r'^(#{1,6}) ', block).group(1))
            content = block[level+1:]  # skip "### "
            children = text_to_children(content)
            block_nodes.append(ParentNode(tag=f'h{level}', children=children))

        elif block_type == Blocktype.CODE:
            code_text = re.sub(r'^```|```$', '', block).strip()
            text_node = TextNode(code_text, TextType.TEXT)
            code_child = text_node_to_html_node(text_node)
            block_nodes.append(ParentNode(tag='pre', children=[
                               ParentNode(tag='code', children=[code_child])]))

        elif block_type == Blocktype.QUOTE:
            content = block[2:] if block.startswith('> ') else block[1:]
            children = text_to_children(content)
            block_nodes.append(ParentNode(tag='blockquote', children=children))

        elif block_type == Blocktype.UNORDERED_LIST:
            items = [line[2:]
                     for line in block.split('\n') if line.startswith('- ')]
            li_nodes = [
                ParentNode(tag='li', children=text_to_children(item)) for item in items]
            block_nodes.append(ParentNode(tag='ul', children=li_nodes))

        elif block_type == Blocktype.ORDERED_LIST:
            items = [re.sub(r'^\d+\. ', '', line)
                     for line in block.split('\n') if re.match(r'^\d+\. ', line)]
            li_nodes = [
                ParentNode(tag='li', children=text_to_children(item)) for item in items]
            block_nodes.append(ParentNode(tag='ol', children=li_nodes))

        elif block_type == Blocktype.PARAGRAPH:
            children = text_to_children(block)
            block_nodes.append(ParentNode(tag='p', children=children))

    return ParentNode(tag='div', children=block_nodes)


def text_to_children(text) -> list[ParentNode]:
    # You should already have this function
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return html_nodes
