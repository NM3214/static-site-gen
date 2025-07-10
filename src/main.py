from textnode import TextNode, TextType
import os
import shutil

def main():
    # test = TextNode("testing", TextType.ITALIC_TEXT, "https://www.boot.dev")
    # print(test)
    #print(os.path.abspath("."))
    copy_to_destination()


def copy_to_destination():
    current_path = os.path.abspath(".")
    public_dir = current_path + "/public/"
    static_dir = current_path + "/static/"
    shutil.rmtree(public_dir)
    os.mkdir(public_dir)

    #print(os.path.join(static_dir, "images/"))
    #shutil.copy(static_dir, current_path)
    

    def inner(rel_path):
        current_path = os.path.join(static_dir, rel_path)
        current_path_public = os.path.join(public_dir, rel_path)
        contents = os.listdir(current_path)
        
        for content in contents:
            path = os.path.join(current_path, content)
            path_public = os.path.join(current_path_public, content)
            if os.path.isdir(path):
                #mkdir publicciin?
                os.mkdir(path_public)
                inner(rel_path + content)
            else:
                shutil.copy(path, path_public)

    inner("")








main()
