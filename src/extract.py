import re

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text) 
    return matches

def extract_title(md):
    for lines in md.split("\n"):
        if lines.startswith("# "):
            header = lines.strip("#").strip()
            return header
    raise Exception(f"NO header found in doc {md[0:10]}...")
        
    