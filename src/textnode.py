from enum import Enum

class TextType(Enum):
    NORMAL_TEXT = "Normal text"
    BOLD_TEXT = "Bold text"
    ITALIC_TEXT = "Italic text"
    CODE_TEXT = "Code text"
    LINKS = "links"
    IMAGES = "Images"

class TextNode:

    def __init__(self, text, text_type, url):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(seld, text_node):
        return text_node.text == self.text and \
                text_node.text_type == self.text_tupe and \
                text_node.url == self.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
