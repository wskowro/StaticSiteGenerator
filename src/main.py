from textnode import TextNode, TextType
from converter import *
from extracttitle import *
import os
import shutil

publicFolder = 'public/'
staticFolder = 'static/'
markdownFile = 'content/index.md'
destinationFile = 'public/index.html'
templateFile = 'template.html'


def main():
    myNode = TextNode("This is some anchor text",
                      TextType.LINK, "https://www.boot.dev")

    delOldPublic(publicFolder)
    generate_page(markdownFile, templateFile, destinationFile)
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
        markdown_file = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template_file = f.read()

    html_node = markdown_to_html_node(markdown_file)
    html_string = html_node.to_html()
    title = extract_title(markdown_file)

    filled_template = template_file.replace("{{ Title }}", title)
    filled_template = filled_template.replace("{{ Content }}", html_string)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(filled_template)


if __name__ == "__main__":
    main()
