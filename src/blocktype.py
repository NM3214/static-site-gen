from enum import Enum
from split_nodes import markdown_to_blocks, text_to_textnodes
from htmlnode import ParentNode
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    QUOTE = "quote"
    CODE = "code"
    UNORDERED_LIST= "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    quote = True
    for line in block.split("\n"):
        if not line.startswith(">"):
            quote = False
            break
    if quote:
        return BlockType.QUOTE
    
    unordered_list = True
    for line in block.split("\n"):
        if not line.startswith("- "):
            unordered_list = False
            break
    if unordered_list:
        return BlockType.UNORDERED_LIST
    
    i = 1
    ordered_list = True
    for line in block.split("\n"):
        if not line.startswith(f"{i}. "):
            ordered_list = False
            break
    if ordered_list:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH



def markdown_to_html_node(markdown):

    def block_to_tag_and_text(block, blocktype):
        match blocktype:
            case BlockType.PARAGRAPH:
                return "p", block
            case BlockType.HEADING:
                text = block.lstrip("#")[1:]
                return f"h{len(block)-len(text)+1}", text
            case BlockType.QUOTE:
                text = "\n".join(list(map(lambda x: x[2:], block.split("\n"))))
                return "blockquote", text
            case BlockType.CODE:
                return "code", block[3:-3]
            case _:
                return None

    def text_to_children(text):
        nodes = text_to_textnodes(text)
        htmlnodes = list(map(text_node_to_html_node, nodes))
        return htmlnodes

    block_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        blocktype = block_to_block_type(block)
        tag_and_text = block_to_tag_and_text(block, blocktype)
        if tag_and_text:
            tag, text = tag_and_text
            if blocktype != BlockType.CODE:
                children = text_to_children(text)
                block_nodes.append(ParentNode(tag, children))
            else:
                child = text_node_to_html_node(TextNode(text, TextType.CODE_TEXT))
                block_nodes.append(ParentNode("pre", [child]))
            
        else:
            match blocktype:
                case BlockType.UNORDERED_LIST:
                    children = []
                    list_items = block.split("\n")
                    for item in list_items:
                        text = item[2:]
                        grandchildren = text_to_children(text)
                        children.append(ParentNode("li", grandchildren))
                    block_nodes.append(ParentNode("ul", children))
                case BlockType.ORDERED_LIST:
                    children = []
                    list_items = block.split("\n")
                    for item in list_items:
                        text = item.split(" ", 1)[1]
                        grandchildren = text_to_children(text)
                        children.append(ParentNode("li", grandchildren))
                    block_nodes.append(ParentNode("ol", children))

    return ParentNode("div", block_nodes)
