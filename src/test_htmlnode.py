import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from markup_to_textnode import extract_markdown_images, split_nodes_image
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("p", "This is a text node", None, { "key": "2", "name": "p-tag"})
        self.assertEqual(node.props_to_html(), " key=2 name=p-tag")
    
    def test_props_to_html_empty(self):
        node = HTMLNode("p", "This is a text node")
        self.assertEqual(node.props_to_html(), "")
    
    def test_repr(self):
        node = HTMLNode("div", "content")
        self.assertEqual(repr(node), "div content")
    
    def test_init_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)


class TestLeafNode(unittest.TestCase):
    def test_to_html_with_tag(self):
        node = LeafNode("p", "This is a paragraph", {"class": "text"})
        self.assertEqual(node.to_html(), "<p class=text>This is a paragraph</p>")
    
    def test_to_html_no_tag(self):
        node = LeafNode(None, "Just some text", {})
        self.assertEqual(node.to_html(), "Just some text")
    
    def test_to_html_empty_value(self):
        node = LeafNode("div", None, {})
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_inheritance(self):
        node = LeafNode("span", "text", {"id": "test"})
        self.assertIsInstance(node, HTMLNode)
        self.assertEqual(node.props_to_html(), " id=test")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child", None)
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild", None)
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
if __name__ == "__main__":
    unittest.main()