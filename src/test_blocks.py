import unittest
from blocktype import BlockType, block_to_block_type, markdown_to_html_node

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_block_to_block_type_heading(self):
        heading_block = "#### This is a heading"
        self.assertEqual(block_to_block_type(heading_block), BlockType.HEADING)

        almost_heading = "-# This is not a heading"
        self.assertEqual(block_to_block_type(almost_heading), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        quote_block = ">This is a quote\n>more of the quote\n> the end"
        self.assertEqual(block_to_block_type(quote_block), BlockType.QUOTE)

        almost_quote = ">This is not a quote\n<This is a paragraph\n>the end"
        self.assertEqual(block_to_block_type(almost_quote), BlockType.PARAGRAPH)

    def test_block_to_block_type_list(self):
        list_block = "- This is a list\n- with items"
        self.assertEqual(block_to_block_type(list_block), BlockType.UNORDERED_LIST)

        almost_list_block = "- This is a list\n- with items\n-text\n- more text"
        self.assertEqual(block_to_block_type(almost_list_block), BlockType.PARAGRAPH)


    def test_markdown_to_html_node_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_markdown_to_html_node_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()