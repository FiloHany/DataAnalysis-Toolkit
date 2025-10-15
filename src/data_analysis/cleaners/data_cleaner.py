"""
Data cleaning utilities following SOLID principles.
Each method has single responsibility for specific cleaning operations.
"""

import pandas as pd
from typing import List, Dict, Any, Optional, Union
import re
from ..config import logger


class DataCleaner:
    """
    Data cleaner class with methods for common data cleaning operations.
    Each method follows Single Responsibility Principle.
    """

    def __init__(self, data: Optional[pd.DataFrame] = None):
        """
        Initialize cleaner with optional data.

        Args:
            data: DataFrame to clean
        """
        self.data = data.copy() if data is not None else None

    def set_data(self, data: pd.DataFrame):
        """Set data for cleaning."""
        self.data = data.copy()
        logger.info(f"Data set for cleaning with shape: {data.shape}")

    def get_data(self) -> Optional[pd.DataFrame]:
        """Get current cleaned data."""
        return self.data

    def remove_duplicates(self) -> pd.DataFrame:
        """
        Remove duplicate rows from data.

        Returns:
            DataFrame with duplicates removed
        """
        if self.data is None:
            raise ValueError("No data set for cleaning")

        original_count = len(self.data)
        self.data = self.data.drop_duplicates()
        removed_count = original_count - len(self.data)

        logger.info(f"Removed {removed_count} duplicate rows")
        return self.data

    def drop_columns(self, columns: List[str]) -> pd.DataFrame:
        """
        Drop specified columns.

        Args:
            columns: List of column names to drop

        Returns:
            DataFrame with columns removed
        """
        if self.data is None:
            raise ValueError("No data set for cleaning")

        self.data = self.data.drop(columns=columns, errors='ignore')
        logger.info(f"Dropped columns: {columns}")
        return self.data

    def clean_text_columns(self, columns: List[str], operations: List[str]) -> pd.DataFrame:
        """
        Clean text in specified columns.

        Args:
            columns: Columns to clean
            operations: List of operations ('strip_chars', 'remove_non_alphanumeric', etc.)

        Returns:
            DataFrame with cleaned text
        """
        if self.data is None:
            raise ValueError("No data set for cleaning")

        for col in columns:
            if col not in self.data.columns:
                logger.warning(f"Column {col} not found, skipping")
                continue

            for op in operations:
                if op == 'strip_chars':
                    chars_to_strip = ['/', '...', '_']
                    for char in chars_to_strip:
                        self.data[col] = self.data[col].str.strip(char)
                elif op == 'remove_non_alphanumeric':
                    self.data[col] = self.data[col].str.replace(r'[^a-zA-Z0-9]', '', regex=True)
                elif op == 'convert_to_string':
                    self.data[col] = self.data[col].astype(str)

        logger.info(f"Cleaned text in columns: {columns}")
        return self.data

    def format_phone_numbers(self, column: str) -> pd.DataFrame:
        """
        Format phone numbers to standard format.

        Args:
            column: Phone number column name

        Returns:
            DataFrame with formatted phone numbers
        """
        if self.data is None:
            raise ValueError("No data set for cleaning")

        if column not in self.data.columns:
            raise ValueError(f"Column {column} not found")

        # Convert to string first
        self.data[column] = self.data[column].astype(str)

        # Remove non-alphanumeric characters
        self.data[column] = self.data[column].str.replace(r'[^a-zA-Z0-9]', '', regex=True)

        # Format as XXX-XXX-XXXX
        def format_phone(phone):
            if len(phone) >= 10:
                return f"{phone[:3]}-{phone[3:6]}-{phone[6:10]}"
            return phone

        self.data[column] = self.data[column].apply(format_phone)

        # Replace empty/nan formats
        self.data[column] = self.data[column].str.replace(r'nan--|Na--', '', regex=True)

        logger.info(f"Formatted phone numbers in column: {column}")
        return self.data

    def split_address_column(self, column: str, new_columns: List[str]) -> pd.DataFrame:
        """
        Split address column into multiple columns.

        Args:
            column: Address column to split
            new_columns: Names for new columns

        Returns:
            DataFrame with split address columns
        """
        if self.data is None:
            raise ValueError("No data set for cleaning")

        if column not in self.data.columns:
            raise ValueError(f"Column {column} not found")

        split_data = self.data[column].str.split(',', expand=True)
        split_data.columns = new_columns[:len(split_data.columns)]

        self.data = pd.concat([self.data, split_data], axis=1)
        logger.info(f"Split {column} into columns: {new_columns}")
        return self.data

    def standardize_categorical_values(self, column: str, mapping: Dict[str, str]) -> pd.DataFrame:
        """
        Standardize categorical values using mapping.

        Args:
            column: Column to standardize
            mapping: Dict mapping old values to new values

        Returns:
            DataFrame with standardized values
        """
        if self.data is None:
            raise ValueError("No data set for cleaning")

        if column not in self.data.columns:
            raise ValueError(f"Column {column} not found")

        self.data[column] = self.data[column].str.replace('|'.join(mapping.keys()),
                                                          lambda m: mapping[m.group()], regex=True)
        logger.info(f"Standardized values in column: {column}")
        return self.data

    def handle_missing_values(self, strategy: str = 'fillna', fill_value: Any = '') -> pd.DataFrame:
        """
        Handle missing values.

        Args:
            strategy: Strategy ('drop', 'fillna', 'interpolate')
            fill_value: Value to fill if using fillna

        Returns:
            DataFrame with handled missing values
        """
        if self.data is None:
            raise ValueError("No data set for cleaning")

        if strategy == 'drop':
            original_count = len(self.data)
            self.data = self.data.dropna()
            logger.info(f"Dropped {original_count - len(self.data)} rows with missing values")
        elif strategy == 'fillna':
            self.data = self.data.fillna(fill_value)
            logger.info(f"Filled missing values with: {fill_value}")
        elif strategy == 'interpolate':
            numeric_cols = self.data.select_dtypes(include=[float, int]).columns
            self.data[numeric_cols] = self.data[numeric_cols].interpolate()
            logger.info("Interpolated missing numeric values")

        return self.data

    def remove_rows_by_condition(self, condition: Union[str, callable]) -> pd.DataFrame:
        """
        Remove rows based on condition.

        Args:
            condition: Condition to filter rows for removal

        Returns:
            DataFrame with rows removed
        """
        if self.data is None:
            raise ValueError("No data set for cleaning")

        original_count = len(self.data)

        if isinstance(condition, str):
            # String condition for query
            rows_to_drop = self.data.query(condition).index
        elif callable(condition):
            # Function condition
            rows_to_drop = self.data[condition(self.data)].index
        else:
            raise ValueError("Condition must be string or callable")

        self.data = self.data.drop(rows_to_drop)
        removed_count = original_count - len(self.data)
        logger.info(f"Removed {removed_count} rows based on condition")
        return self.data

    def reset_index_clean(self) -> pd.DataFrame:
        """Reset index and drop old index."""
        if self.data is None:
            raise ValueError("No data set for cleaning")

        self.data = self.data.reset_index(drop=True)
        logger.info("Reset index")
        return self.data
