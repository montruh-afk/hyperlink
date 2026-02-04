from textnode import TextNode, TextType
from extract import *
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for nodes in old_nodes:
        if nodes.text_type != TextType.TEXT or delimiter not in nodes.text:
            new_nodes.append(nodes)
        
        else:
            split = nodes.text.split(delimiter)
            if (len(split) - 1) % 2 != 0:
                raise Exception("invalid markdown syntax.")
            for i in range(len(split)):
                if i % 2 == 0:
                    split[i] = TextNode(split[i], TextType.TEXT)
                elif i % 2 != 0:
                    split[i] = TextNode(split[i], text_type)
            
            new_nodes.extend(split)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = extract_markdown_links(text)

        if not matches:
            new_nodes.append(node)
            continue

        for alt, url in matches:
            before, after = text.split(f"[{alt}]({url})", 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, url))
            text = after  # continue from the remaining text

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes
                

        

        

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = extract_markdown_images(text)

        if not matches:
            new_nodes.append(node)
            continue

        for alt, url in matches:
            before, after = text.split(f"![{alt}]({url})", 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = after  # continue from the remaining text

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes