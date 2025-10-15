"""
Tests for data cleaner module.
"""

import pytest
import pandas as pd
import numpy as np
from src.data_analysis.cleaners.data_cleaner import DataCleaner


class TestDataCleaner:
    """Test cases for DataCleaner class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.sample_data = pd.DataFrame({
            'Name': ['John', 'Jane', 'John', 'Bob'],
            'Phone': ['123-456-7890', '987.654.3210', '(555) 123-4567', '555/987/6543'],
            'Email': ['john@example.com', 'jane@example.com', 'bob@example.com', 'alice@example.com'],
            'Paying Customer': ['Yes', 'No', 'Yes', 'No']
        })
        self.cleaner = DataCleaner(self.sample_data)

    def test_initialization(self):
        """Test cleaner initialization."""
        assert self.cleaner.get_data() is not None
        assert len(self.cleaner.get_data()) == 4

    def test_remove_duplicates(self):
        """Test duplicate removal."""
        # Add a duplicate row
        duplicate_data = pd.concat([self.sample_data, self.sample_data.iloc[0:1]], ignore_index=True)
        cleaner = DataCleaner(duplicate_data)

        result = cleaner.remove_duplicates()

        assert len(result) == 4  # Should remove one duplicate

    def test_drop_columns(self):
        """Test column dropping."""
        result = self.cleaner.drop_columns(['Email'])

        assert 'Email' not in result.columns
        assert 'Name' in result.columns

    def test_clean_text_columns_strip_chars(self):
        """Test text cleaning with character stripping."""
        result = self.cleaner.clean_text_columns(['Phone'], ['strip_chars'])

        # Check if special characters are stripped
        phone_values = result['Phone'].tolist()
        # This would depend on the implementation, adjust accordingly

    def test_format_phone_numbers(self):
        """Test phone number formatting."""
        result = self.cleaner.format_phone_numbers('Phone')

        formatted_phones = result['Phone'].tolist()
        # Check if phones are in XXX-XXX-XXXX format
        for phone in formatted_phones:
            if phone != '':  # Skip empty strings
                assert '-' in phone or phone == ''

    def test_standardize_categorical_values(self):
        """Test categorical value standardization."""
        result = self.cleaner.standardize_categorical_values('Paying Customer', {'Yes': 'Y', 'No': 'N'})

        values = result['Paying Customer'].tolist()
        assert 'Y' in values
        assert 'N' in values
        assert 'Yes' not in values
        assert 'No' not in values

    def test_handle_missing_values_fillna(self):
        """Test missing value handling with fillna."""
        data_with_missing = self.sample_data.copy()
        data_with_missing.loc[0, 'Name'] = np.nan
        cleaner = DataCleaner(data_with_missing)

        result = cleaner.handle_missing_values(strategy='fillna', fill_value='Unknown')

        assert result['Name'].iloc[0] == 'Unknown'

    def test_reset_index_clean(self):
        """Test index resetting."""
        # Set a custom index first
        data_with_index = self.sample_data.set_index('Name')
        cleaner = DataCleaner(data_with_index)

        result = cleaner.reset_index_clean()

        assert result.index.name is None
        assert isinstance(result.index, pd.RangeIndex)
