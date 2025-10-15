"""
Example: Data cleaning pipeline
Demonstrates the data cleaning module usage.
"""

import pandas as pd
from src.data_analysis.cleaners import DataCleaner

def create_sample_data():
    """Create sample messy data for demonstration."""
    data = {
        'Name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown'],
        'Phone': ['123-456-7890', '987.654.3210', '(555) 123-4567', '555/987/6543'],
        'Email': ['john@example.com', 'jane@example.com', 'bob@example.com', 'alice@example.com'],
        'Paying Customer': ['Yes', 'No', 'Yes', 'No'],
        'Do_Not_Contact': ['Y', 'N', 'Y', 'N']
    }
    return pd.DataFrame(data)

def main():
    # Create sample data
    df = create_sample_data()
    print("Original data:")
    print(df)

    # Initialize cleaner
    cleaner = DataCleaner(df)

    # Clean phone numbers
    cleaner.clean_text_columns(['Phone'], ['remove_non_alphanumeric'])
    cleaner.format_phone_numbers('Phone')

    # Standardize categorical values
    cleaner.standardize_categorical_values('Paying Customer', {'Yes': 'Y', 'No': 'N'})

    # Get cleaned data
    cleaned_df = cleaner.get_data()
    print("\nCleaned data:")
    print(cleaned_df)

    # Save cleaned data
    cleaned_df.to_csv('cleaned_customer_data.csv', index=False)
    print("\nCleaned data saved to 'cleaned_customer_data.csv'")

if __name__ == "__main__":
    main()
