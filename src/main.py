from textnode import TextNode, TextType


def main():
    myNode = TextNode("This is some anchor text",
                      TextType.LINK, "https://www.boot.dev")
    print(myNode)


if __name__ == "__main__":
    main()
