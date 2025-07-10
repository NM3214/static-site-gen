import unittest
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_somthing(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        expected = [
    TextNode("This is text with a ", TextType.PLAIN_TEXT),
    TextNode("code block", TextType.CODE_TEXT),
    TextNode(" word", TextType.PLAIN_TEXT),
]
        self.assertEqual(new_nodes, expected)

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN_TEXT),
                TextNode("bolded", TextType.BOLD_TEXT),
                TextNode(" word", TextType.PLAIN_TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.PLAIN_TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN_TEXT),
                TextNode("bolded", TextType.BOLD_TEXT),
                TextNode(" word and ", TextType.PLAIN_TEXT),
                TextNode("another", TextType.BOLD_TEXT),
            ],
            new_nodes,
        )


    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], extract_markdown_images(text))




    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], extract_markdown_links(text))


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


    def test_split_links(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.PLAIN_TEXT,
    )
        new_nodes = split_nodes_link([node])
    
        self.assertListEqual(
            [
            TextNode("This is text with a link ", TextType.PLAIN_TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.PLAIN_TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ],
            new_nodes,
        )

        node2 = TextNode(
        "[to boot dev](https://www.boot.dev) and that is all",
        TextType.PLAIN_TEXT,
    )
        new_nodes2 = split_nodes_link([node2])
        self.assertListEqual(
            [
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and that is all", TextType.PLAIN_TEXT)
        ],
            new_nodes2,
        )

        self.assertListEqual(
            [
            TextNode("This is text with a link ", TextType.PLAIN_TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.PLAIN_TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and that is all", TextType.PLAIN_TEXT)
        ],
            split_nodes_link([node, node2]),
        )


    def test_text_to_textnodes(self):
        markdown = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(markdown)
        self.assertListEqual(
            [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.PLAIN_TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ],
            nodes
        )


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

if __name__ == "__main__":
    unittest.main()