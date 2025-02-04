

from bs4 import BeautifulSoup
from typing import List, Dict

class ContentCleaning:
    
    def clean_html(self, html_content: str) -> str:
        """Clean HTML content and extract meaningful text"""
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            
            # Remove unwanted elements
            for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
                element.decompose()

            # Get text content
            text = soup.get_text(separator="\n", strip=True)
            
            # Additional cleaning
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            return "\n".join(lines)
        
        except Exception as e:
            # self.logger.error(f"HTML cleaning failed: {str(e)}")
            return html_content  # Return original content as fallback