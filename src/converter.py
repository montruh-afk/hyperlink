from htmlnode import *
from textnode import *
from parser import *
from splitter import *

def ol_to_node(block):
    list_item_nodes = []
    items = parsing_ol(block) 

    for item_text in items:
        if item_text is None or item_text.strip() == "":
            continue

        inline_html_children = []
        for tn in text_to_textnodes(item_text):
            child = text_node_to_html_node(tn)
            if child is None:
                continue
            inline_html_children.append(child)

    # now use inline_html_children to build the <li> node

                    
        li_node = ParentNode("li", inline_html_children)

                    
        list_item_nodes.append(li_node)

                
    ol_block_node = ParentNode("ol", list_item_nodes)
    return ol_block_node

def ul_to_node(block):
    list_item_nodes = [] # This list will hold all the <li> HTMLNodes
    items = parsing_ul(block) # Get your clean item strings

    for item_text in items:
        if item_text is None or item_text.strip() == "":
            continue

        inline_html_children = []
        for tn in text_to_textnodes(item_text):
            child = text_node_to_html_node(tn)
            if child is None:
                continue
            inline_html_children.append(child)

    # now use inline_html_children to build the <li> node

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
    html_children = []
    for tn in text_nodes:
        html_child = text_node_to_html_node(tn)
        if html_child is None:
            continue
        html_children.append(html_child)

    return html_children, hash_dict[str(hashes)]

def quote_to_node(block):
    quote = parsing_quotes(block)
    if not quote:
        return None
    html_children = []
    text_node = text_to_textnodes(quote)
    for tn in text_node:
        html_child = text_node_to_html_node(tn)
        if html_child is None:
            continue
        html_children.append(html_child)
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
        if blocks is None or blocks.strip() == "":
            continue
        text_node = text_to_textnodes(blocks)
        for nodes in text_node:
            html_child = text_node_to_html_node(nodes)
            if html_child is None:
                continue
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