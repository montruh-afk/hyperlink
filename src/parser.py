import re

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