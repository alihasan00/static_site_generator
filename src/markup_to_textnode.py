from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            new_nodes.extend(break_string(old_node, delimiter, text_type))
        else:
            new_nodes.append(old_node)
    return new_nodes


def break_string(node, delimiter, text_type):
    text = node.text
    parts = []
    result = []
    
    is_inside = False
    start = 0
    
    i = 0
    while i < len(text):
        if text[i:i+len(delimiter)] == delimiter:
            if is_inside:
                parts.append((text[start:i], text_type if is_inside else node.text_type))
            else:
                parts.append((text[start:i], node.text_type))
            
            i += len(delimiter)
            start = i
            is_inside = not is_inside
        else:
            i += 1
    
    if start < len(text):
        parts.append((text[start:], text_type if is_inside else node.text_type))
    
    for text_part, type_part in parts:
        if text_part:
            result.append(TextNode(text_part, type_part))
    
    return result


def extract_markdown_images(text):
    image_reg = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(image_reg, text)

def extract_markdown_links(text):
    image_reg = r"\[(.*?)\]\((.*?)\)"
    return re.findall(image_reg, text)

def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        text = node.text
        for index, link in enumerate(links):
            sub_text = text.split(f"[{link[0]}]({link[1]})", 1)
            result.append(TextNode(sub_text[0], node.text_type))
            result.append(TextNode(link[0], TextType.LINK, link[1]))
            text = sub_text[-1]
            if index == len(links) - 1 and len(text) != 0 and text != result[-1].text:
                result.append(TextNode(text, node.text_type))
        if not links:
            result.append(node)
    return result

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        text = node.text
        for index, image in enumerate(images):
            sub_text = text.split(f"![{image[0]}]({image[1]})", 1)
            result.append(TextNode(sub_text[0], node.text_type))
            result.append(TextNode(image[0], TextType.IMAGE, image[1]))
            text = sub_text[-1]
            if index == len(images) - 1 and len(text) != 0 and text != result[-1].text:
                result.append(TextNode(text, node.text_type))
        if not images:
            result.append(node)
    return result
