from blocktype import markdown_to_html_node
import os

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line[:2] == "# ":
            return line[2:].strip()
    raise Exception("No title found in markdown file")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown = f.read()
    
    with open(template_path) as f:
        template = f.read()

    html_text = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    
    template = template.replace("{{ Title }}", title, 1).replace("{{ Content }}", html_text, 1)

    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
  
    for f in os.listdir(dir_path_content):
        path_content = os.path.join(dir_path_content, f)
        path_destination = os.path.join(dest_dir_path, f)
        if os.path.isdir(path_content):
            generate_pages_recursive(path_content, template_path, path_destination)
        else:
            dest = path_destination[:-2] + "html"
            generate_page(path_content, template_path, dest)

