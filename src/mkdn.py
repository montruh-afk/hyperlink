from block_type import *
from htmlnode import *
from splitter import *
import re

def markdown_to_blocks(markdown):
    parts = markdown.split("\n\n")
    blocks = []
    for part in parts:
        part = part.strip()
        if part == "":
            continue
        blocks.append(part)
    return blocks

def parsing_ul(block):
    raw_list_items = []
    current_item_content = ""
    block = block.strip()
    for line in block.split("\n"):
        if line.startswith("- ") or line.startswith("* ") or line.startswith("+ "):
            if current_item_content: # If there's a previous item, append it
                raw_list_items.append(current_item_content)
            current_item_content = line[1:].strip() # Start new item, remove marker & strip
        else:
            # Handle continuation lines
            current_item_content += f" {line.strip()}"
    if current_item_content: # Append the last item after the loop
        raw_list_items.append(current_item_content)
    return raw_list_items
                
                
def parsing_ol(block):
    raw_list_items = []
    current_item_content = ""
    for line in block.split("\n"):
        digit = re.match(r"^\d+\. ", line)
        if digit is not None:
            length = len(digit.group(0))
            if current_item_content:
                raw_list_items.append(current_item_content)
            current_item_content = line[length:]
        else:
            current_item_content += f' {line.strip()}'
    if current_item_content:
        raw_list_items.append(current_item_content)
    return raw_list_items
            
def parsing_quotes(block):
    clean_lines = []
    for quotes in block.split("\n"):
        clean_lines.append(quotes[1:].strip())
    return " ".join(clean_lines)
    
def parsing_paragraphs(block):
    clean_lines = []
    lines = ""
    for paragraph in block.split("\n\n"):
        chars = paragraph.split()
        for char in chars:
            if char != "\n":
                lines += f' {char}'
            else:
                continue
        clean_lines.append(lines.strip())
    
    return clean_lines

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    
    
    
    return nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                html_children = []
                clean_block = parsing_paragraphs(block)
                for blocks in clean_block:
                    text_node = text_to_textnodes(blocks)
                    for nodes in text_node:
                        html_children.append(text_node_to_html_node(nodes))

                block_nodes.append(ParentNode("p", html_children))
            case BlockType.CODE:
                block = block.strip("```")
                code_node = TextNode(block[1:] if block.startswith("\n") else block, TextType.TEXT)
                child = text_node_to_html_node(code_node)  # Convert TextNode to HTMLNode
                parent = ParentNode("code", [child])  # Wrap in <code> ParentNode
                block_nodes.append(ParentNode("pre", [parent]))  # Wrap in <pre>
            case BlockType.HEADING:
                hash_dict = {"1": "h1", 
                            "2": "h2", 
                            "3": "h3", 
                            "4": "h4", 
                            "5": "h5", 
                            "6": "h6", 
                            }
                hashes = len(re.match(r"^#+", block).group(0))
                if hashes > 6 or hashes < 1:
                    raise ValueError(f"invalid markdown header format: Text contains {hashes} hashes")
                block = block[hashes:]
                text_nodes = text_to_textnodes(block.strip())
                html_children = [text_node_to_html_node(nodes) for nodes in text_nodes]
                block_nodes.append(ParentNode(hash_dict[f"{hashes}"], html_children))
                
            case BlockType.QUOTE:
                quote = parsing_quotes(block)
                text_node = text_to_textnodes(quote)
                html_children = [text_node_to_html_node(nodes) for nodes in text_node]
                block_nodes.append(ParentNode("blockquote", html_children))
                        
            case BlockType.UNORDERED_LIST:
                list_item_nodes = [] # This list will hold all the <li> HTMLNodes
                items = parsing_ul(block) # Get your clean item strings

                for item_text in items: # For each clean item string:
                    # 1. Convert the item's text into a list of HTMLNode children for the <li>
                    inline_html_children = [text_node_to_html_node(tn) for tn in text_to_textnodes(item_text)]

                    # 2. Create an <li> ParentNode using these children
                    li_node = ParentNode("li", inline_html_children)

                    # 3. Add this <li> node to our list_item_nodes 
                    list_item_nodes.append(li_node)

                # 4. Finally, create the <ul> ParentNode using all the <li> nodes
                ul_block_node = ParentNode("ul", list_item_nodes)

                # 5. Add the <ul> block node to your main block_nodes list
                block_nodes.append(ul_block_node)
                    
            case BlockType.ORDERED_LIST:
                list_item_nodes = []
                items = parsing_ol(block) 

                for item_text in items:
                    inline_html_children = [text_node_to_html_node(tn) for tn in text_to_textnodes(item_text)]

                    
                    li_node = ParentNode("li", inline_html_children)

                    
                    list_item_nodes.append(li_node)

                
                ol_block_node = ParentNode("ol", list_item_nodes)

                
                block_nodes.append(ol_block_node)
    final_html = ParentNode("div", block_nodes)
    return final_html