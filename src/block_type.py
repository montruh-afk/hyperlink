from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"
    
    
def block_to_block_type(markdown_block):
    lines = markdown_block.split("\n")
    
    if markdown_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
            return BlockType.HEADING
    
    if markdown_block.startswith("```\n") and markdown_block.endswith("```"):
        return BlockType.CODE
    
    if markdown_block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    if all(line.startswith("- ") or line.startswith("* ") or line.startswith("+ ")for line in lines):
        return BlockType.UNORDERED_LIST

    if markdown_block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

    