from block_type import *
from converter import *

def markdown_to_blocks(markdown):
    parts = markdown.split("\n\n")
    blocks = []
    for part in parts:
        part = part.strip()
        if part == "":
            continue
        blocks.append(part)
    return blocks





def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                html_children = paragraph_to_node(block)
                children = []
                for child in html_children:
                    if child is None or child == "":
                        continue
                    children.append(child)

                block_nodes.append(ParentNode("p", children))
            case BlockType.CODE:
                parent = code_to_node(block)
                block_nodes.append(ParentNode("pre", [parent]))  # Wrap in <pre>
            case BlockType.HEADING:
                html_children, hash_ = heading_to_node(block)
                block_nodes.append(ParentNode(hash_, html_children))
                
            case BlockType.QUOTE:
                html_children = quote_to_node(block)
                block_nodes.append(ParentNode("blockquote", html_children))
                        
            case BlockType.UNORDERED_LIST:
                ul_block_node = ul_to_node(block)

                # 5. Add the <ul> block node to your main block_nodes list
                block_nodes.append(ul_block_node)
                    
            case BlockType.ORDERED_LIST:
                ol_block_node = ol_to_node(block)

                
                block_nodes.append(ol_block_node)
    
    final_html = ParentNode("div", block_nodes)
    return final_html