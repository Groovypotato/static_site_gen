from enum import Enum
from ex_mrkdn_lnk import extract_markdown_images,extract_markdown_links
import re
from htmlnode import HTMLNode,ParentNode,LeafNode
import textwrap


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
        if text_node.text_type == TextType.TEXT:
            return LeafNode(None,text_node.text)
        elif text_node.text_type == TextType.BOLD:
            return LeafNode("b",text_node.text)
        elif text_node.text_type == TextType.ITALIC:
            return LeafNode("i",text_node.text)
        elif text_node.text_type == TextType.CODE:
            return LeafNode("code",text_node.text)
        elif text_node.text_type == TextType.LINK:
            return LeafNode("a",text_node.text,{"href":text_node.url})
        elif text_node.text_type == TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        else:
            raise Exception("This node does not have a Valid 'TextType'")
    
def split_nodes_image(old_nodes):
    new_list = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            links = extract_markdown_images(node.text)
            if links == []:
                new_list.append(node)
            else:
                text = node.text
                for title,url in links:
                    text = text.split(f"![{title}]({url})", 1)
                    if len(text[0]) > 0:
                        new_list.append(TextNode(text[0], TextType.TEXT))
                    new_list.append(TextNode(title, TextType.IMAGE, url))
                    text = text[1]
                if text != "":
                    new_list.append(TextNode(text, TextType.TEXT))
        else:
            new_list.append(node)                  
    return new_list



def split_nodes_link(old_nodes):
    new_list = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            links = extract_markdown_links(node.text)
            if links == []:
                new_list.append(node)
            else:
                text = node.text
                for link,url in links:
                    text = text.split(f"[{link}]({url})", 1)
                    if len(text[0]) > 0:
                        new_list.append(TextNode(text[0], TextType.TEXT))
                    new_list.append(TextNode(link, TextType.LINK, url))
                    text = text[1]
                if text != "":
                    new_list.append(TextNode(text, TextType.TEXT))
        else:
            new_list.append(node)
    return new_list
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
        else:
            if delimiter not in node.text:
                new_list.append(node)
            else:
                split_delim = node.text.split(delimiter)
                for i,chunk in enumerate(split_delim):
                    if i % 2 > 0:
                        new_list.append(TextNode(chunk,text_type))
                    else:
                        new_list.append(TextNode(chunk,TextType.TEXT))

    return new_list

def text_to_textnodes(text):
    node = [TextNode(text,TextType.TEXT)]
    return split_nodes_delimiter(split_nodes_delimiter(split_nodes_image(split_nodes_link(split_nodes_delimiter(node,"`",TextType.CODE))),"**", TextType.BOLD),"_",TextType.ITALIC)


def markdown_to_blocks(markdown):
    blocks = []
    split_text = markdown.split("\n\n")
    for block in split_text:
        blocks.append(block.strip())
    return blocks

def block_to_block_type(markdown_text):
    heading_pattern = r'^[#]{1,6} '
    quote_pattern = r'^>'
    unordered_list_pattern = r'^(-|\*)'
    ordered_list_pattern = r'^(\d+)\. '
    if re.match(heading_pattern,markdown_text):
        return BlockType.HEADING
    if markdown_text.startswith("```") and markdown_text.endswith("```"):
        return BlockType.CODE
    split = markdown_text.splitlines()
    if all(re.match(quote_pattern,line) for line in split):
        return BlockType.QUOTE
    elif all(re.match(unordered_list_pattern,line) for line in split):
        return BlockType.UNORDERED_LIST
    ordered_list = True
    for idx, line in enumerate(split, start=1):
        match = re.match(ordered_list_pattern, line)
        if not match or int(match.group(1)) != idx:
            ordered_list = False
            break
    if ordered_list:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def text_to_childeren(text):
    children = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children
    
def markdown_to_html_node(markdown):
    nodes = []
    tag_dict = {
        BlockType.HEADING:"h",
        BlockType.CODE: "code",
        BlockType.QUOTE: "blockquote",
        BlockType.ORDERED_LIST: "ol",
        BlockType.UNORDERED_LIST: "ul",
        BlockType.PARAGRAPH: "p",
    }
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if not block.strip():
            continue
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            h_count = 0 
            for char in block[0:5]:
                if char == "#":
                    h_count += 1
            node = LeafNode(tag_dict[block_type]+str(h_count),block[h_count+1:].strip())
            nodes.append(node)
        elif block_type == BlockType.QUOTE:
            split = block.splitlines()
            new_lines = []
            for line in split:
                if line.startswith("> "):
                    new_lines.append(line[2:].strip())
                elif line.startswith(">"):
                    new_lines.append(line[1:].strip())
            new_text = "\n".join(new_lines)
            node = ParentNode(tag_dict[block_type],children=text_to_childeren(new_text))
            nodes.append(node)
        elif block_type == BlockType.CODE:
            clean_text = block[3:-3].strip("\n")
            clean_text = textwrap.dedent(clean_text)
            node = ParentNode("pre", children=[text_node_to_html_node(TextNode(clean_text, TextType.CODE))])
            nodes.append(node)
        elif block_type == BlockType.UNORDERED_LIST:
            split = block.splitlines()
            lines = []
            for line in split:
                if line.startswith("- ") or line.startswith("* "):
                    content = line[2:].strip()
                else:
                    content = line.strip()
                lines.append(content)
            list_items = []
            for line in lines:
                list_items.append(ParentNode("li",children=text_to_childeren(line)))
            node = ParentNode(tag_dict[block_type],children=list_items)
            nodes.append(node)
        elif block_type == BlockType.ORDERED_LIST:
            split = block.splitlines()
            lines = []
            pattern = r"^(\d+)\. "
            for line in split:
                match = re.match(pattern, line)
                if match:
                    content = line[match.end():].strip()
                else:
                    content = line.strip()
                lines.append(content)
            list_items = []
            for line in lines:
                list_items.append(ParentNode("li",children=text_to_childeren(line)))
            node = ParentNode(tag_dict[block_type],children=list_items)
            nodes.append(node)
        elif block_type == BlockType.PARAGRAPH:
            clean_block = re.sub(r"\s+", " ", block.strip())
            children = text_to_childeren(clean_block)
            node = ParentNode(tag_dict[block_type],children=children)
            nodes.append(node)
    return ParentNode("div",children=nodes)


def extract_title(markdown):
    lines = markdown.splitlines()
    if lines[0].startswith("# "):
        return lines[0][2:].strip()
    else:
        raise Exception("Ain't no header1 in this bitch")
