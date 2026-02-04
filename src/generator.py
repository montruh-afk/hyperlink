from mkdn import *
import os, os.path as path
from extract import extract_title




def generate_page(from_path, template_path, dest_path):
    print(f'Generating path from {from_path} to {dest_path} using {template_path}')
    
    from_path = path.abspath(from_path)
    template_path = path.abspath(template_path)
    dest_path = path.abspath(dest_path)
    
    if path.isdir(from_path) or not path.exists(from_path):
        raise OSError("The file to write from does not exist")
    
    elif path.isdir(template_path) or not path.exists(template_path):
        raise OSError("Missing template file")
    
    elif not path.exists(path.dirname(dest_path)):
        os.makedirs(path.dirname(dest_path))
    
    
    with open(from_path, "r", encoding="utf-8") as f:
        file_content = f.read()
        f.close()
    
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
        f.close()
            
    markdown = markdown_to_html_node(file_content).to_html()
    title = extract_title(file_content)
    
    html = template.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", markdown)       
            
    with open(dest_path, "w") as f:
        length = f.write(html)
    
        