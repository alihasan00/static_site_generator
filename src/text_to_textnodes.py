from textnode import TextNode, TextType
from markup_to_textnode import split_nodes_image, split_nodes_link, split_nodes_delimiter

delimiters = dict({
    TextType.BOLD: "**",
    TextType.ITALIC: "_",
    TextType.CODE: "`",
    TextType.IMAGE: "![",
    TextType.LINK: "[",
})

def text_to_textnodes(text):
    node = [TextNode(text, TextType.TEXT)]

    for text_type, delimiter in delimiters.items():
        if text_type == TextType.IMAGE:
            node = split_nodes_image(node)
        elif text_type == TextType.LINK:
            node = split_nodes_link(node)
        else:
            node = split_nodes_delimiter(node, delimiter, text_type)
    return node