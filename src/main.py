from generate_page import generate_pages_recursive
import os
import shutil
import sys

def main():

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    


    current_path = os.path.abspath(".")
    content = current_path + "/content/"
    static = current_path + "/static/"
    template = current_path + "/template.html"
    destination = current_path + "/docs/"
    copy_to_destination(static, destination)
    
    generate_pages_recursive(content, template, destination, basepath)




def copy_to_destination(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)


    def inner(rel_path):
        current_path = os.path.join(source, rel_path)
        current_path_public = os.path.join(destination, rel_path)
        contents = os.listdir(current_path)
        
        for content in contents:
            path = os.path.join(current_path, content)
            path_public = os.path.join(current_path_public, content)
            if os.path.isdir(path):
                os.mkdir(path_public)
                inner(rel_path + content)
            else:
                shutil.copy(path, path_public)

    inner("")

    








main()
