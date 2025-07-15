import unittest

from textnode import TextNode, TextType, text_to_textnodes,split_nodes_image,split_nodes_link,split_nodes_delimiter,markdown_to_blocks,BlockType,block_to_block_type,markdown_to_html_node,text_node_to_html_node,extract_title



class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node,node2)

    def test_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2) 
    
    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
    
    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")
    
    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
    
    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK,"https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href":"https://www.boot.dev"})
        

    def test_image(self):
        node = TextNode("This is a image node", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.boot.dev", "alt": "This is a image node"})

    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)   
        self.assertEqual(new_nodes,[TextNode("This is text with a ", TextType.TEXT),TextNode("code block", TextType.CODE),TextNode(" word", TextType.TEXT),])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
    )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
                )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
    )
    
    def test_text2_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual([
                        TextNode("This is ", TextType.TEXT),
                        TextNode("text", TextType.BOLD),
                        TextNode(" with an ", TextType.TEXT),
                        TextNode("italic", TextType.ITALIC),
                        TextNode(" word and a ", TextType.TEXT),
                        TextNode("code block", TextType.CODE),
                        TextNode(" and an ", TextType.TEXT),
                        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                        TextNode(" and a ", TextType.TEXT),
                        TextNode("link", TextType.LINK, "https://boot.dev"),
                        ],nodes)

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
    def test_blocktype_heading(self):
        heading1 = block_to_block_type(markdown_to_blocks("# this is a heading with 1 #")[0])
        heading2 = block_to_block_type(markdown_to_blocks("## this is a heading with 2 #")[0])
        heading3 = block_to_block_type(markdown_to_blocks("### this is a heading with 3 #")[0])
        heading4 = block_to_block_type(markdown_to_blocks("#### this is a heading with 4 #")[0])
        heading5 = block_to_block_type(markdown_to_blocks("##### this is a heading with 5 #")[0])
        heading6 = block_to_block_type(markdown_to_blocks("###### this is a heading with 6 #")[0])
        heading7 = block_to_block_type(markdown_to_blocks("####### this is a heading with 7 #")[0])
        self.assertEqual(heading1,BlockType.HEADING)
        self.assertEqual(heading2,BlockType.HEADING)
        self.assertEqual(heading3,BlockType.HEADING)
        self.assertEqual(heading4,BlockType.HEADING)
        self.assertEqual(heading5,BlockType.HEADING)
        self.assertEqual(heading6,BlockType.HEADING)
        self.assertIsNot(heading7,BlockType.HEADING)
    
    def test_blocktype_code(self):
        code_block1 = block_to_block_type(markdown_to_blocks("```This is a code block```")[0])
        code_block2 = block_to_block_type(markdown_to_blocks("```This is a code block")[0])
        code_block3 = block_to_block_type(markdown_to_blocks("This is a code block```")[0])
        self.assertEqual(code_block1,BlockType.CODE)
        self.assertIsNot(code_block2,BlockType.CODE)
        self.assertIsNot(code_block3,BlockType.CODE)
        
    def test_blocktype_quote(self):
        quote_block1 = block_to_block_type(markdown_to_blocks(">This is a quote block")[0])
        quote_block2 = block_to_block_type(markdown_to_blocks(">This is a quote block\n>This is a quote block\n>This is a quote block")[0])
        quote_block3 = block_to_block_type(markdown_to_blocks(">This is a quote block\n>This is a quote block\nThis is a quote block")[0])
        self.assertEqual(quote_block1,BlockType.QUOTE)
        self.assertEqual(quote_block2,BlockType.QUOTE)
        self.assertIsNot(quote_block3,BlockType.QUOTE)

    def test_blocktype_unordered_list(self):
        uo_list_block1 = block_to_block_type(markdown_to_blocks("- This is a unordered list block")[0])
        uo_list_block2 = block_to_block_type(markdown_to_blocks("- This is a unordered list block\n- This is a unordered list block\n- This is a unordered list block")[0])
        uo_list_block3 = block_to_block_type(markdown_to_blocks("- This is a unordered list block\n- This is a unordered list block\nThis is a unordered list block")[0])
        self.assertEqual(uo_list_block1,BlockType.UNORDERED_LIST)
        self.assertEqual(uo_list_block2,BlockType.UNORDERED_LIST)
        self.assertIsNot(uo_list_block3,BlockType.UNORDERED_LIST)

    def test_blocktype_ordered_list(self):
        o_list_block1 = block_to_block_type(markdown_to_blocks("1. This is a unordered list block")[0])
        o_list_block2 = block_to_block_type(markdown_to_blocks("1. This is a unordered list block\n2. This is a unordered list block\n3. This is a unordered list block")[0])
        o_list_block3 = block_to_block_type(markdown_to_blocks("1. This is a unordered list block\n3. This is a unordered list block\n2. This is a unordered list block")[0])
        o_list_block4 = block_to_block_type(markdown_to_blocks("3. This is a unordered list block\n2. This is a unordered list block\n1. This is a unordered list block")[0])
        self.assertEqual(o_list_block1,BlockType.ORDERED_LIST)
        self.assertEqual(o_list_block2,BlockType.ORDERED_LIST)
        self.assertIsNot(o_list_block3,BlockType.ORDERED_LIST)
        self.assertIsNot(o_list_block4,BlockType.ORDERED_LIST)

    def test_blocktype_paragraph(self):
        paragraph1 = block_to_block_type(markdown_to_blocks("This is a paragraph block")[0])
        paragraph2 = block_to_block_type(markdown_to_blocks("####### this is not a heading with 7 #")[0])
        paragraph3 = block_to_block_type(markdown_to_blocks("```This is not a code block")[0])
        paragraph4 = block_to_block_type(markdown_to_blocks(">This is not a quote block\n>This is not a quote block\nThis is not a quote block")[0])
        paragraph5 = block_to_block_type(markdown_to_blocks("- This is not a unordered list block\n- This is not a unordered list block\nThis is not a unordered list block")[0])
        paragraph6 = block_to_block_type(markdown_to_blocks("3. This is not a unordered list block\n2. This is not a unordered list block\n1. This not is a unordered list block")[0])
        paragraph7 = block_to_block_type(markdown_to_blocks("```This is not a paragraph block```")[0])
        self.assertEqual(paragraph1,BlockType.PARAGRAPH)
        self.assertEqual(paragraph2,BlockType.PARAGRAPH)
        self.assertEqual(paragraph3,BlockType.PARAGRAPH)
        self.assertEqual(paragraph4,BlockType.PARAGRAPH)
        self.assertEqual(paragraph5,BlockType.PARAGRAPH)
        self.assertEqual(paragraph6,BlockType.PARAGRAPH)
        self.assertIsNot(paragraph7,BlockType.PARAGRAPH)

    def test_paragraphs(self):
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

    def test_codeblock(self):
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

    def test_extract_title(self):
        header1 = extract_title("# Hello")
        header2 = extract_title("## Hello")
        header3 = extract_title("Hello")
        header4 = extract_title("#Hello")
        self.assertEqual(header1,"Hello")
        self.assertIsNot(header2,"Hello")
        self.assertIsNot(header3,"Hello")
        self.assertIsNot(header4,"Hello")

if __name__ == "__main__":
    unittest.main()