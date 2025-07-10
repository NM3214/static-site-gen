from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            result.append(node)
            continue
        split = node.text.split(delimiter)
        if len(split) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for new_node_i in range(len(split)):
            if split[new_node_i] == "":
                continue
            if new_node_i % 2 == 0:
                result.append(TextNode(split[new_node_i], TextType.PLAIN_TEXT))
            else:
                result.append(TextNode(split[new_node_i], text_type))
    return result


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!  )\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            result.append(node)
            continue
        original_text = node.text
        images = extract_markdown_images(original_text)
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.PLAIN_TEXT))
            result.append(TextNode(image[0], TextType.IMAGE, image[1]))
            original_text = sections[1]
        if original_text != "":
            result.append(TextNode(original_text, TextType.PLAIN_TEXT))
    return result


def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            result.append(node)
            continue
        original_text = node.text
        links = extract_markdown_links(original_text)
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.PLAIN_TEXT))
            result.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            result.append(TextNode(original_text, TextType.PLAIN_TEXT))
    return result


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN_TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = list(map(lambda x: x.strip(), blocks))
    return list(filter(lambda x: x != "", blocks))