import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

        node3 = TextNode("This is a textnode", TextType.CODE_TEXT, "www.com")
        node4 = TextNode("This is a textnode", TextType.CODE_TEXT, "www.com")
        self.assertEqual(node3, node4)

        node5 = TextNode("This is a text node", TextType.BOLD_TEXT)
        node6 = TextNode("This is a text node", TextType.BOLD_TEXT, "link")
        self.assertNotEqual(node5, node6)

        node7 = TextNode("This is a text node", TextType.BOLD_TEXT)
        node8 = TextNode("This is a text node", TextType.ITALIC_TEXT)
        self.assertNotEqual(node7, node8)

    def test_repr(self):
        repr_text = repr(TextNode("This is a text node", TextType.LINK, "www.com"))
        self.assertEqual("TextNode(This is a text node, link, www.com)", repr_text)

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        node2 = TextNode("This is an image", TextType.IMAGE, "www.com")
        html_node2 = text_node_to_html_node(node2)
        self.assertEqual(html_node2.tag, "img")
        self.assertEqual(html_node2.value, "")
        self.assertEqual(html_node2.props, {"src": "www.com", "alt": "This is an image"})

if __name__ == "__main__":
    unittest.main()