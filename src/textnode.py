from enum import Enum

class TextType(Enum):
    TEXT = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'


class TextNode:

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, obj):
        return self.text == obj.text and \
            self.url == obj.url and \
            self.text_type == obj.text_type
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})" 