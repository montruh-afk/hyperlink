from mkdn import *
import os, os.path as path
from extract import extract_title




def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    
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
            
    html_node = markdown_to_html_node(file_content)
    content_html = html_node.to_html()
    title = extract_title(file_content)
    
    html = template.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", content_html)       
            
    with open(dest_path, "w") as f:
        length = f.write(html)
        
def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    entry = os.listdir(dir_path_content)
    for i in entry:
        if path.isfile(path.join(dir_path_content, i)):
            if i.endswith(".md"):
                generate_page(path.join(dir_path_content, i), template_path, path.join(dest_dir_path, i.replace(".md", ".html")))
            else:
                continue
        elif path.isdir(path.join(dir_path_content, i)):
            new_dest_dir_path = path.join(dest_dir_path, i)
            if not path.exists(new_dest_dir_path):
                os.mkdir(new_dest_dir_path)
            generate_page_recursive(path.join(dir_path_content, i), template_path, new_dest_dir_path)
    
        