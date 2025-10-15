"""
Crypto API client for fetching cryptocurrency data.
Follows SOLID principles with single responsibility for API interactions.
"""

import requests
from requests.exceptions import RequestException
import json
import pandas as pd
import time
from typing import Dict, List, Optional, Any
import os
from ..config import logger, CRYPTO_API_KEY, CRYPTO_API_URL, DEFAULT_TIMEOUT


class CryptoAPI:
    """
    API client for cryptocurrency data from CoinMarketCap.
    Handles authentication, rate limiting, and data collection.
    """

    def __init__(self, api_key: Optional[str] = None, timeout: int = DEFAULT_TIMEOUT):
        """
        Initialize API client.

        Args:
            api_key: CoinMarketCap API key
            timeout: Request timeout
        """
        self.api_key = api_key or CRYPTO_API_KEY
        if not self.api_key:
            raise ValueError("API key required. Set CMC_API_KEY environment variable or pass api_key.")

        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.api_key
        })

        self.base_url = CRYPTO_API_URL
        self.last_request_time = 0
        self.rate_limit_delay = 60  # seconds between requests for free tier

    def _rate_limit_wait(self):
        """Implement rate limiting."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit_delay:
            wait_time = self.rate_limit_delay - elapsed
            logger.info(f"Rate limiting: waiting {wait_time:.1f} seconds")
            time.sleep(wait_time)
        self.last_request_time = time.time()

    def _make_request(self, params: Dict[str, Any]) -> Optional[Dict]:
        """
        Make API request with error handling.

        Args:
            params: Request parameters

        Returns:
            JSON response data or None if failed
        """
        self._rate_limit_wait()

        try:
            response = self.session.get(self.base_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            logger.info(f"API request successful: {len(data.get('data', []))} records")
            return data
        except RequestException as e:
            logger.error(f"API request failed: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return None

    def get_listings(self, start: int = 1, limit: int = 15, convert: str = 'USD') -> pd.DataFrame:
        """
        Get cryptocurrency listings.

        Args:
            start: Starting rank
            limit: Number of results
            convert: Currency to convert to

        Returns:
            DataFrame with crypto data
        """
        params = {
            'start': start,
            'limit': limit,
            'convert': convert
        }

        data = self._make_request(params)
        if not data or 'data' not in data:
            return pd.DataFrame()

        df = pd.json_normalize(data['data'])
        df['timestamp'] = pd.to_datetime('now')
        logger.info(f"Retrieved {len(df)} cryptocurrency listings")
        return df

    def run_automated_collection(self, cycles: int = 333, interval: int = 60,
                               output_file: str = 'crypto_data.csv') -> pd.DataFrame:
        """
        Run automated data collection with rate limiting.

        Args:
            cycles: Number of collection cycles
            interval: Seconds between cycles
            output_file: Output CSV file path

        Returns:
            Combined DataFrame of all collected data
        """
        all_data = pd.DataFrame()

        for i in range(cycles):
            logger.info(f"Collection cycle {i+1}/{cycles}")

            df = self.get_listings()
            if df.empty:
                logger.warning(f"Empty data in cycle {i+1}, skipping")
                continue

            # Append to combined data
            all_data = pd.concat([df, all_data], ignore_index=True)

            # Save to file
            if not os.path.isfile(output_file):
                df.to_csv(output_file, index=False, header='column_names')
            else:
                df.to_csv(output_file, index=False, mode='a', header=False)

            if i < cycles - 1:  # Don't sleep after last cycle
                logger.info(f"Waiting {interval} seconds before next cycle")
                time.sleep(interval)

        logger.info(f"Automated collection complete: {len(all_data)} total records")
        return all_data

    def clean_crypto_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and prepare crypto data for analysis.

        Args:
            df: Raw crypto DataFrame

        Returns:
            Cleaned DataFrame
        """
        # Remove non-numeric header rows
        numeric_cols = ['quote.USD.percent_change_1h', 'quote.USD.percent_change_24h',
                       'quote.USD.percent_change_7d', 'quote.USD.percent_change_30d',
                       'quote.USD.percent_change_60d', 'quote.USD.percent_change_90d']

        for col in numeric_cols:
            if col in df.columns:
                df = df[pd.to_numeric(df[col], errors='coerce').notna()]

        # Convert percentage columns to float
        for col in numeric_cols:
            if col in df.columns:
                df[col] = df[col].astype(float)

        logger.info(f"Cleaned crypto data: {len(df)} records")
        return df

    def calculate_price_changes(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate price change statistics by cryptocurrency.

        Args:
            df: Cleaned crypto DataFrame

        Returns:
            DataFrame with price change aggregations
        """
        change_cols = ['quote.USD.percent_change_1h', 'quote.USD.percent_change_24h',
                      'quote.USD.percent_change_7d', 'quote.USD.percent_change_30d',
                      'quote.USD.percent_change_60d', 'quote.USD.percent_change_90d']

        available_cols = [col for col in change_cols if col in df.columns]

        if not available_cols:
            logger.warning("No price change columns found")
            return pd.DataFrame()

        grouped = df.groupby('name', sort=False)[available_cols].mean()
        logger.info(f"Calculated price changes for {len(grouped)} cryptocurrencies")
        return grouped

    def get_bitcoin_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract Bitcoin-specific data.

        Args:
            df: Crypto DataFrame

        Returns:
            DataFrame with Bitcoin data only
        """
        bitcoin_data = df[df['name'] == 'Bitcoin'][['name', 'quote.USD.price', 'timestamp']]
        logger.info(f"Extracted {len(bitcoin_data)} Bitcoin records")
        return bitcoin_data
