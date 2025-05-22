from textnode import TextNode, TextType
from leafnode import LeafNode
from extractmarkdown import *
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
