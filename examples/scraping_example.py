"""
Example: Web scraping companies data
Demonstrates the web scraping module usage.
"""

from src.data_analysis.scrapers import WebScraper
from src.data_analysis.processors import PandasProcessor

def main():
    # Initialize scraper
    scraper = WebScraper()

    # Scrape companies data
    url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'
    companies_df = scraper.scrape_companies_list(url)

    print(f"Scraped {len(companies_df)} companies")
    print(companies_df.head())

    # Process the data
    processor = PandasProcessor()
    processor.set_data(companies_df)

    # Filter top 10 companies
    top_10 = processor.filter_data("Rank <= 10")
    print(f"\nTop 10 companies:\n{top_10}")

    # Save to CSV
    processor.save_csv('top_companies.csv')

if __name__ == "__main__":
    main()
