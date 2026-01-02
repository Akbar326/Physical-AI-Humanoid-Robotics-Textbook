import asyncio
import requests
from typing import List
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import logging

from .logging import app_logger


class SitemapParser:
    """
    A utility class for parsing sitemaps and extracting URLs.
    """

    def __init__(self, sitemap_url: str):
        self.sitemap_url = sitemap_url

    async def get_urls(self) -> List[str]:
        """
        Fetch and parse the sitemap to extract URLs.
        """
        urls = []
        try:
            app_logger.info(f"Fetching sitemap from: {self.sitemap_url}")

            response = requests.get(self.sitemap_url, timeout=30)
            response.raise_for_status()

            # Parse the sitemap XML
            soup = BeautifulSoup(response.content, 'xml')

            # Check if this is a sitemap index (sitemap of sitemaps)
            sitemap_tags = soup.find_all('sitemap')
            if sitemap_tags:
                app_logger.info("Found sitemap index, processing multiple sitemaps")
                for sitemap_tag in sitemap_tags:
                    loc = sitemap_tag.find('loc')
                    if loc:
                        nested_sitemap_url = loc.text.strip()
                        app_logger.info(f"Processing nested sitemap: {nested_sitemap_url}")
                        nested_urls = await self._get_urls_from_sitemap(nested_sitemap_url)
                        urls.extend(nested_urls)
            else:
                # This is a regular sitemap with URLs
                app_logger.info("Processing regular sitemap")
                urls = await self._get_urls_from_sitemap(self.sitemap_url)

            app_logger.info(f"Extracted {len(urls)} URLs from sitemap(s)")
            return urls

        except Exception as e:
            app_logger.error(f"Error parsing sitemap: {str(e)}")
            raise

    async def _get_urls_from_sitemap(self, sitemap_url: str) -> List[str]:
        """
        Helper method to extract URLs from a single sitemap.
        """
        urls = []
        try:
            response = requests.get(sitemap_url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'xml')

            # Find all URL entries
            url_tags = soup.find_all('url')

            for url_tag in url_tags:
                loc = url_tag.find('loc')
                if loc:
                    url = loc.text.strip()
                    urls.append(url)

            return urls

        except Exception as e:
            app_logger.error(f"Error parsing sitemap {sitemap_url}: {str(e)}")
            raise