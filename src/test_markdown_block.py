import unittest
from markdown_to_blocks import markdown_to_blocks
from markdown_block import block_to_block_type, BlockType


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestMarkdownBlock(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a normal paragraph with no special formatting."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
    def test_heading(self):
        blocks = [
            "# Heading 1",
            "## Heading 2",
            "### Heading 3",
            "#### Heading 4",
            "##### Heading 5",
            "###### Heading 6"
        ]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)
            
    def test_not_heading(self):
        # No space after #
        block = "#Not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
    def test_code(self):
        blocks = [
            "```\ncode block\n```",
            "```python\ndef hello():\n    print('world')\n```"
        ]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), BlockType.CODE)
            
    def test_quote(self):
        blocks = [
            ">This is a quote",
            ">Line 1\n>Line 2\n>Line 3"
        ]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
            
    def test_not_quote(self):
        # Not all lines start with >
        block = ">Line 1\nLine 2\n>Line 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
            
    def test_unordered_list(self):
        blocks = [
            "- Item 1",
            "- Item 1\n- Item 2\n- Item 3"
        ]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), BlockType.ULIST)
            
    def test_not_unordered_list(self):
        # Not all lines start with -
        block = "- Item 1\nNot an item\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
            
    def test_ordered_list(self):
        blocks = [
            "1. Item 1",
            "1. Item 1\n2. Item 2\n3. Item 3"
        ]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), BlockType.OLIST)
            
    def test_not_ordered_list_wrong_sequence(self):
        # Not sequential
        block = "1. Item 1\n3. Item 2\n4. Item 3" 
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
    def test_not_ordered_list_wrong_start(self):
        # Doesn't start with 1
        block = "2. Item 1\n3. Item 2\n4. Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
