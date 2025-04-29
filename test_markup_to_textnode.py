import unittest
from textnode import TextNode, TextType
from markup_to_textnode import split_nodes_delimiter


class TestMarkupToTextNode(unittest.TestCase):
    def test_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    
    def test_bold_text(self):
        node = TextNode("This is text with **bold words** in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold words")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " in it")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    
    def test_italic_text(self):
        node = TextNode("This is text with _italic words_ in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "italic words")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " in it")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    
    def test_multiple_delimiters(self):
        node = TextNode("Text with `code` and **bold** words", TextType.TEXT)
        # First process code blocks
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        # Then process bold text in the result
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "Text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "bold")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[4].text, " words")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)
    
    def test_nested_delimiters(self):
        node = TextNode("Text with **bold and `code` inside**", TextType.TEXT)
        # First process bold
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        # Then process code blocks in the result
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold and ")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, "code inside")  # This test will actually fail
        self.assertEqual(new_nodes[2].text_type, TextType.CODE)  # This shows a limitation
    
    def test_non_text_nodes_preserved(self):
        nodes = [
            TextNode("Regular text", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("More text with `code`", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "Regular text")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "Already bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, "More text with ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "code")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)
    
    def test_no_delimiters(self):
        node = TextNode("Text with no delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Text with no delimiters")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
    
    def test_unclosed_delimiter(self):
        node = TextNode("Text with unclosed `delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "Text with unclosed ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "delimiter")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)


if __name__ == "__main__":
    unittest.main() 