import os
import html2text
from bs4 import BeautifulSoup
import re

class HtmlToMarkdownPipeline:
    def __init__(self):
        # Initialize the HTML to Markdown converter
        self.converter = html2text.HTML2Text()
        self.converter.ignore_links = True
        self.converter.ignore_images = True
        self.converter.body_width = 0  # Prevents line wrapping for clean markdown
        
        # Ensure the directory for saving Markdown files exists
        self.output_dir = 'markdown_files'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def remove_header_footer(self, html_content):
        """
        Remove <header> and <footer> tags from the HTML content.
        """
        # Parse HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove <header> and <footer> tags
        for tag in soup(['header', 'footer']):
            tag.decompose()
        
        # Return the cleaned HTML as a string
        return str(soup)

    def remove_emojis(self, text):
        """
        Remove all emojis from the text.
        """
        # Regex pattern to match emojis
        emoji_pattern = re.compile(
            "["  
            "\U0001F600-\U0001F64F"  # Emoticons
            "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
            "\U0001F680-\U0001F6FF"  # Transport & Map Symbols
            "\U0001F700-\U0001F77F"  # Alchemical Symbols
            "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
            "\U0001F800-\U0001F8FF"  # Supplemental Arrows Extended
            "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            "\U0001FA00-\U0001FA6F"  # Chess Symbols
            "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
            "\U00002702-\U000027B0"  # Dingbats
            "\U000024C2-\U0001F251"  # Enclosed Characters
            "]+", 
            flags=re.UNICODE
        )
        return emoji_pattern.sub(r'', text)

    def clean_markdown(self, markdown_content):
        """
        Clean the markdown content to ensure it's well-structured and readable.
        """
        # Remove leading/trailing spaces
        cleaned_content = markdown_content.strip()
        
        # Remove excessive line breaks by replacing multiple consecutive newlines with a single newline
        cleaned_content = re.sub(r'\n{3,}', '\n\n', cleaned_content)
        
        # Remove carriage return characters
        cleaned_content = cleaned_content.replace('\r', '')
        
        # Remove consecutive spaces
        cleaned_content = re.sub(r' {2,}', ' ', cleaned_content)
        
        # Remove non-ASCII characters
        cleaned_content = re.sub(r'[^\x00-\x7F]+', '', cleaned_content)
        
        return cleaned_content

    def process_item(self, item, spider):
        # Get the HTML content from the item
        html_content = item.get('body_html', '')
        
        # Remove <header> and <footer> tags from HTML content
        if html_content:
            html_content = self.remove_header_footer(html_content)
            
            # Remove emojis from the HTML content
            html_content = self.remove_emojis(html_content)
            
            # Convert HTML to Markdown
            markdown_content = self.converter.handle(html_content)

            # Clean and structure the markdown content
            markdown_content = self.clean_markdown(markdown_content)

            # Save Markdown content to file
            title = item.get('title', 'default')
            file_name = f"{title}.md"
            file_path = os.path.join(self.output_dir, file_name)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(markdown_content)

            # Optionally, update item to include file path or Markdown content
            item['body_html'] = markdown_content
        
        # Return the updated item
        return item
