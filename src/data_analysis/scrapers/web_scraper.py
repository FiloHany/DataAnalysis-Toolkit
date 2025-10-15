"""
Web scraper for collecting data from web sources.
Follows Single Responsibility Principle - handles only web scraping.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import pandas as pd
from ..config import logger, DEFAULT_TIMEOUT


class WebScraper:
    """
    Web scraper class for extracting data from web pages.
    Uses requests and BeautifulSoup for HTML parsing.
    """

    def __init__(self, timeout: int = DEFAULT_TIMEOUT):
        """
        Initialize the web scraper.

        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()

    def get_page_content(self, url: str) -> Optional[str]:
        """
        Fetch HTML content from a URL.

        Args:
            url: Target URL to scrape

        Returns:
            HTML content as string, or None if failed
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            logger.info(f"Successfully fetched content from {url}")
            return response.text
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None

    def parse_table_to_dataframe(self, html_content: str, table_index: int = 0) -> pd.DataFrame:
        """
        Parse HTML table into pandas DataFrame.

        Args:
            html_content: HTML content containing tables
            table_index: Index of table to parse (default: 0)

        Returns:
            DataFrame with table data
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        tables = soup.find_all('table')

        if not tables:
            logger.warning("No tables found in HTML content")
            return pd.DataFrame()

        if table_index >= len(tables):
            logger.warning(f"Table index {table_index} out of range. Using first table.")
            table_index = 0

        table = tables[table_index]

        # Extract headers
        headers = []
        header_row = table.find('thead')
        if header_row:
            headers = [th.text.strip() for th in header_row.find_all('th')]
        else:
            # Try first row as headers
            first_row = table.find('tr')
            if first_row:
                headers = [th.text.strip() for th in first_row.find_all(['th', 'td'])]

        # Extract data rows
        rows = []
        for row in table.find_all('tr')[1:]:  # Skip header row
            cells = row.find_all(['td', 'th'])
            row_data = [cell.text.strip() for cell in cells]
            if row_data:
                rows.append(row_data)

        # Create DataFrame
        df = pd.DataFrame(rows, columns=headers if headers else None)
        logger.info(f"Parsed table with {len(df)} rows and {len(df.columns)} columns")
        return df

    def scrape_companies_list(self, url: str) -> pd.DataFrame:
        """
        Scrape list of largest companies from Wikipedia.

        Args:
            url: Wikipedia URL for companies list

        Returns:
            DataFrame with companies data
        """
        html_content = self.get_page_content(url)
        if not html_content:
            return pd.DataFrame()

        df = self.parse_table_to_dataframe(html_content, table_index=0)

        # Set Rank as index if exists
        if 'Rank' in df.columns:
            df.set_index('Rank', inplace=True)

        return df
