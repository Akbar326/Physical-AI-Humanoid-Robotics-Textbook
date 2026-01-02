import requests
from typing import Tuple
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import logging

from .logging import app_logger


class ContentExtractor:
    """
    A utility class for extracting content from URLs.
    """

    @staticmethod
    def extract_content_from_url(url: str, timeout: int = 30) -> Tuple[str, str]:
        """
        Extract title and content from a URL.
        Returns a tuple of (title, content).
        """
        try:
            app_logger.info(f"Extracting content from: {url}")

            response = requests.get(url, timeout=timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Try to find main content areas in Docusaurus sites
            main_content = None

            # Look for common Docusaurus content selectors
            selectors = [
                'main div[class*="docItemContainer"]',
                'article',
                'main div[class*="container"]',
                'div[class*="doc"]',
                'main',
                'div[class*="theme"]'
            ]

            for selector in selectors:
                main_content = soup.select_one(selector)
                if main_content:
                    break

            # If no specific content area found, use body
            if not main_content:
                main_content = soup.find('body')

            # Extract text content
            content = main_content.get_text() if main_content else soup.get_text()

            # Clean up the text
            lines = (line.strip() for line in content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            content = ' '.join(chunk for chunk in chunks if chunk)

            # Extract title
            title_tag = soup.find('title')
            title = title_tag.get_text().strip() if title_tag else urlparse(url).path.split('/')[-1] or 'Untitled'

            app_logger.info(f"Successfully extracted content from {url}: title='{title[:50]}...', content_len={len(content)}")
            return title, content

        except Exception as e:
            app_logger.error(f"Error extracting content from {url}: {str(e)}")
            return "", ""