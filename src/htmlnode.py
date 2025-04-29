class HTMLNode:

    def __init__(self, tag =None, value = None, children = None, props = None) -> None:
        self.tag = tag
        self.value = value
        self.props = props
        self.children = children
    
    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        htmlProps = ""
        if not self.props: return htmlProps
        for key, value in self.props.items():
            htmlProps += (f" {key}={value}")
        return htmlProps
    
    def __repr__(self) -> str:
        return f"{self.tag} {self.value}"

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        # Handle empty values gracefully
        if not self.tag:
            return self.value or ""
        
        if self.tag == "img":
            return f"<{self.tag}{super().props_to_html()}>"
        
        return f"<{self.tag}{super().props_to_html()}>{self.value or ''}</{self.tag}>"

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag cannot be empty!")
        if self.children is None:
            raise ValueError("Children cannot be None!")
        html = ''
        for child in self.children:
            html += child.to_html()
        return f"<{self.tag}{super().props_to_html()}>{html}</{self.tag}>"


