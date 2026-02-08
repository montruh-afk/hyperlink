from textnode import *
from extract import *
from splitter import *
from htmlnode import *
import os.path as path, os
import shutil
from generator import generate_page_recursive
import sys

def copy(initial, destination):
    if not path.exists(destination):
        os.mkdir(destination)
    for dirs in os.listdir(initial):
        initial_path = path.join(initial, dirs)
        destination_path = path.join(destination, dirs)
        if path.isfile(initial_path):
            copy_ = shutil.copy(initial_path, destination_path)
            continue
        elif not path.exists(destination_path):
            os.mkdir(destination_path)
        copy(initial_path, destination_path)


def main():
    basepath = sys.argv[1]
    src = path.abspath("static")
    dst = path.abspath("docs")
    
    if path.exists(src) and path.isdir(src):
        if path.exists(dst):
            shutil.rmtree(dst)
        os.mkdir(dst)
        copy(src, dst)
    else:
        raise FileNotFoundError(f"{src} must exist and be a directory")
    generate_page_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()