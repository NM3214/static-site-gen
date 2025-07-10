from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    PLAIN_TEXT = "plain text"
    BOLD_TEXT = "bold text"
    ITALIC_TEXT = "italic text"
    CODE_TEXT = "code text"
    LINK= "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.PLAIN_TEXT:
            return LeafNode(None, text_node.text.replace("\n", " "))
        case TextType.BOLD_TEXT:
            return LeafNode("b", text_node.text.replace("\n", " "))
        case TextType.ITALIC_TEXT:
            return LeafNode("i", text_node.text.replace("\n", " "))
        case TextType.CODE_TEXT:
            return LeafNode("code", text_node.text.lstrip())
        case TextType.LINK:
            return LeafNode("a", text_node.text.replace("\n", " "), {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text.replace("\n", " ")})
        case _:
            raise ValueError(f"invalid text type: {text_node.text_type}")