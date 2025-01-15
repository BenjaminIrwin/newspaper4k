import logging
from typing import List, Optional
import lxml
from newspaper.configuration import Configuration
import newspaper.parsers as parsers
from newspaper.urls import urljoin_if_valid

log = logging.getLogger(__name__)


class LinkExtractor:
    """Extractor class for links within articles. Gets all links that appear
    within the main article content."""

    def __init__(self, config: Configuration) -> None:
        """Initialize the link extractor

        Args:
            config (Configuration): Configuration object containing settings
        """
        self.config = config
        self.links: List[str] = []  # List of URLs

    def parse(
        self, doc: lxml.html.Element, top_node: lxml.html.Element, article_url: str
    ) -> None:
        """Main method to extract links from a document

        Args:
            doc (lxml.html.Element): Full HTML document
            top_node (lxml.html.Element): Main article content node
            article_url (str): URL of the article being parsed
        """
        if top_node is None:
            return

        # Get all links within the article body
        self.links = self._get_article_links(top_node, article_url)

    def _get_article_links(
        self, top_node: lxml.html.Element, article_url: str
    ) -> List[str]:
        """Extract all links from within the article body

        Args:
            top_node (lxml.html.Element): Main article content node
            article_url (str): URL of the article being parsed

        Returns:
            List[str]: List of URLs found in the article
        """
        links = []
        for link in parsers.get_tags(top_node, tag="a"):
            href = link.get("href")
            if not href:
                continue

            # Skip empty or javascript links
            if not href.strip() or href.startswith(("javascript:", "#", "mailto:")):
                continue

            # Make URL absolute if it's relative
            absolute_url = urljoin_if_valid(article_url, href)
            if absolute_url:
                links.append(absolute_url)

        return links

    def get_links(self) -> List[str]:
        """Get all extracted links

        Returns:
            List[str]: List of URLs
        """
        return self.links 