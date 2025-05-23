from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, target):
        if self.text == target.text and self.text_type == target.text_type and self.url == target.url:
            return True
        else:
            return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_to_textnodes(text: str) -> list[TextNode]:
    pattern = r'(\*\*.*?\*\*|_.*?_|`.*?`)'
    segments = re.split(pattern, text)
    nodes = []

    for segment in segments:
        if segment.startswith('**') and segment.endswith('**'):
            nodes.append(TextNode(segment[2:-2], "bold"))
        elif segment.startswith('_') and segment.endswith('_'):
            nodes.append(TextNode(segment[1:-1], "italic"))
        elif segment.startswith('`') and segment.endswith('`'):
            nodes.append(TextNode(segment[1:-1], "code"))
        else:
            if segment:  # skip empty
                nodes.append(TextNode(segment, "text"))
    return nodes
