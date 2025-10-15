"""
Refactored version of the original notebook using the new modular package.
This demonstrates how to use the professional data analysis package.
"""

import pandas as pd
from src.data_analysis.scrapers.web_scraper import WebScraper
from src.data_analysis.cleaners.data_cleaner import DataCleaner
from src.data_analysis.processors.pandas_processor import PandasProcessor
from src.data_analysis.eda.exploratory_analysis import EDAAnalyzer
from src.data_analysis.api.crypto_api import CryptoAPI
from src.data_analysis.visualization.plotter import Plotter

def main():
    """Main workflow demonstrating the refactored functionality."""

    print("=== Professional Data Analysis Package Demo ===\n")

    # 1. Web Scraping Section
    print("1. Web Scraping: Largest Companies in the US")
    scraper = WebScraper()
    url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'
    companies_df = scraper.scrape_companies_list(url)
    print(f"Scraped {len(companies_df)} companies")
    print(companies_df.head())
    print()

    # 2. Data Processing Section
    print("2. Data Processing: Pandas Operations")
    processor = PandasProcessor()

    # Load sample data (replace with actual file path)
    try:
        # world_population_df = processor.load_csv('/content/world_population.csv')
        # For demo, create sample data
        sample_data = pd.DataFrame({
            'Country': ['China', 'India', 'USA', 'Indonesia', 'Brazil'],
            'Rank': [1, 2, 3, 4, 5],
            'Population': [1444216107, 1393409038, 331002651, 273523615, 212559417]
        })

        # Filtering
        top_countries = processor.filter_by_rank(sample_data, rank_threshold=3)
        print("Top 3 countries by rank:")
        print(top_countries)
        print()

        # Indexing
        indexed_df = processor.set_index(sample_data, 'Country')
        print("Data indexed by Country:")
        print(indexed_df.head())
        print()

    except Exception as e:
        print(f"Data processing demo skipped: {e}")
        print()

    # 3. Data Cleaning Section
    print("3. Data Cleaning: Phone Numbers and Text")
    sample_customer_data = pd.DataFrame({
        'Name': ['John', 'Jane', 'John', 'Bob'],
        'Phone': ['123-456-7890', '987.654.3210', '(555) 123-4567', '555/987/6543'],
        'Email': ['john@example.com', 'jane@example.com', 'bob@example.com', 'alice@example.com'],
        'Paying Customer': ['Yes', 'No', 'Yes', 'No']
    })

    cleaner = DataCleaner(sample_customer_data)

    # Clean phone numbers
    cleaned_df = cleaner.format_phone_numbers('Phone')
    print("Cleaned phone numbers:")
    print(cleaned_df[['Name', 'Phone']])
    print()

    # Standardize categorical values
    standardized_df = cleaner.standardize_categorical_values('Paying Customer', {'Yes': 'Y', 'No': 'N'})
    print("Standardized categorical values:")
    print(standardized_df[['Name', 'Paying Customer']])
    print()

    # 4. EDA Section
    print("4. Exploratory Data Analysis")
    analyzer = EDAAnalyzer(sample_data)

    # Basic statistics
    stats = analyzer.get_basic_stats()
    print("Basic statistics:")
    print(stats)
    print()

    # 5. Crypto API Section
    print("5. Crypto API: Automated Data Collection")
    crypto_api = CryptoAPI()

    # Note: This would require actual API keys and running the API
    print("Crypto API initialized (requires API keys for full functionality)")
    print()

    # 6. Visualization Section
    print("6. Data Visualization")
    plotter = Plotter()

    # Create sample data for visualization
    viz_data = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [2, 4, 6, 8, 10],
        'category': ['A', 'B', 'A', 'B', 'A']
    })

    print("Visualization plotter initialized")
    print("Sample data prepared for plotting")
    print()

    print("=== Demo Complete ===")
    print("The package provides modular, SOLID-compliant data analysis tools.")
    print("Each module has a single responsibility and can be used independently.")

if __name__ == "__main__":
    main()
