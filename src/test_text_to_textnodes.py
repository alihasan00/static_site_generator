import unittest

from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_complex(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        
        actual_result = text_to_textnodes(text)
        
        self.assertEqual(len(expected_result), len(actual_result))
        for i in range(len(expected_result)):
            self.assertEqual(expected_result[i], actual_result[i])
    
    # def test_text_to_textnodes_single_bold(self):
    #     text = "This is **bold** text"
    #     expected_result = [
    #         TextNode("This is ", TextType.TEXT),
    #         TextNode("bold", TextType.BOLD),
    #         TextNode(" text", TextType.TEXT),
    #     ]
        
    #     actual_result = text_to_textnodes(text)
        
    #     self.assertEqual(len(expected_result), len(actual_result))
    #     for i in range(len(expected_result)):
    #         self.assertEqual(expected_result[i], actual_result[i])
    
    # def test_text_to_textnodes_plain_text(self):
    #     text = "Just plain text"
    #     expected_result = [
    #         TextNode("Just plain text", TextType.TEXT),
    #     ]
        
    #     actual_result = text_to_textnodes(text)
        
    #     self.assertEqual(len(expected_result), len(actual_result))
    #     for i in range(len(expected_result)):
    #         self.assertEqual(expected_result[i], actual_result[i])


if __name__ == "__main__":
    unittest.main() 