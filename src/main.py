from textnode import TextNode, TextType
from converter import *
from extracttitle import *
import os
import shutil

publicFolder = 'public'
staticFolder = 'static'
markdownFile = 'content/index.md'
destinationFile = 'public/index.html'
templateFile = 'template.html'
content_dir = 'content'


def main():
    myNode = TextNode("This is some anchor text",
                      TextType.LINK, "https://www.boot.dev")

    delOldPublic(publicFolder)
    generate_pages_recursive(content_dir, templateFile, publicFolder)
    copySiteContents(staticFolder, publicFolder)

    print(myNode)


def delOldPublic(dest):
    if not os.path.exists(dest):
        os.makedirs(dest)
    for filename in os.listdir(dest):
        file_path = os.path.join(dest, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def copySiteContents(src, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            copySiteContents(s, d)
        else:
            shutil.copy2(s, d)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {
          dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    title = extract_title(markdown_content)

    filled_template = template_content.replace("{{ Title }}", title)
    filled_template = filled_template.replace("{{ Content }}", html_content)

    # ✅ Ensure parent directories exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(filled_template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                # Full path to source markdown file
                md_path = os.path.join(root, file)

                # Relative path inside content directory
                rel_path = os.path.relpath(md_path, dir_path_content)

                # Change .md to .html and build destination path
                rel_html_path = os.path.splitext(rel_path)[0] + ".html"
                dest_path = os.path.join(dest_dir_path, rel_html_path)

                print(f"Generating page from {md_path} to {
                      dest_path} using {template_path}")
                generate_page(md_path, template_path, dest_path)


if __name__ == "__main__":
    main()
