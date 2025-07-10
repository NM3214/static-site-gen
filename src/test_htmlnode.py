import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {
    "href": "https://www.google.com",
    "target": "_blank",
}
        node = HTMLNode("h1", "test value", None, props)
        expected_props_to_html = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_props_to_html)

        node2 = HTMLNode()
        expected_props_to_html2 = ""
        self.assertEqual(node2.props_to_html(), expected_props_to_html2)

    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        node2 = LeafNode("a", "This is a paragraph of text.")
        self.assertEqual(node2.to_html(), "<a>This is a paragraph of text.</a>")

        node3 = LeafNode("div", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node3.to_html(), '<div href="https://www.google.com">Click me!</div>')
        
        node4 = LeafNode(None, "Hello, world!")
        self.assertEqual(node4.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()