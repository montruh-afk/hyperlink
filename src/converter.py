from htmlnode import *
from textnode import *
from parser import *
from splitter import *

def ol_to_node(block):
    list_item_nodes = []
    items = parsing_ol(block) 

    for item_text in items:
        inline_html_children = [text_node_to_html_node(tn) for tn in text_to_textnodes(item_text)]

                    
        li_node = ParentNode("li", inline_html_children)

                    
        list_item_nodes.append(li_node)

                
    ol_block_node = ParentNode("ol", list_item_nodes)
    return ol_block_node

def ul_to_node(block):
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
    return ul_block_node

def heading_to_node(block):
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
    return html_children, hash_dict[f"{hashes}"]

def quote_to_node(block):
    quote = parsing_quotes(block)
    text_node = text_to_textnodes(quote)
    html_children = [text_node_to_html_node(nodes) for nodes in text_node]
    return html_children

def code_to_node(block):
    block = block.strip("```")
    code_node = TextNode(block[1:] if block.startswith("\n") else block, TextType.TEXT)
    child = text_node_to_html_node(code_node)  # Convert TextNode to HTMLNode
    parent = ParentNode("code", [child])
    return parent
    
def paragraph_to_node(block):
    html_children = []
    clean_block = parsing_paragraphs(block)
    for blocks in clean_block:
        text_node = text_to_textnodes(blocks)
        for nodes in text_node:
            html_children.append(text_node_to_html_node(nodes))
    return html_children

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    
    
    
    return nodes