"""
Example: Complete data analysis workflow
Demonstrates using all modules together in a comprehensive analysis.
"""

from src.data_analysis.scrapers import WebScraper
from src.data_analysis.processors import PandasProcessor
from src.data_analysis.cleaners import DataCleaner
from src.data_analysis.eda import EDAAnalyzer
from src.data_analysis.visualization import Plotter
import matplotlib.pyplot as plt

def main():
    print("=== Data Analysis Toolkit: Complete Workflow Demo ===\n")

    # Step 1: Web Scraping
    print("1. Web Scraping: Collecting companies data...")
    scraper = WebScraper()
    url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'
    companies_df = scraper.scrape_companies_list(url)
    print(f"   Scraped {len(companies_df)} companies\n")

    # Step 2: Data Processing
    print("2. Data Processing: Filtering and sorting...")
    processor = PandasProcessor()
    processor.set_data(companies_df)

    # Filter top companies and sort by revenue
    top_companies = processor.filter_data("Rank <= 20")
    sorted_companies = processor.sort_data('Rank')
    print(f"   Processed {len(sorted_companies)} top companies\n")

    # Step 3: Data Cleaning (if needed)
    print("3. Data Cleaning: Ensuring data quality...")
    cleaner = DataCleaner(sorted_companies)
    cleaned_data = cleaner.remove_duplicates().get_data()
    print(f"   Cleaned data has {len(cleaned_data)} records\n")

    # Step 4: Exploratory Data Analysis
    print("4. EDA: Analyzing data patterns...")
    analyzer = EDAAnalyzer(cleaned_data)

    print("   Summary Statistics:")
    summary = analyzer.get_summary_statistics()
    print(f"   {summary.shape[0]} numeric columns analyzed")

    print("   Missing Values Check:")
    missing = analyzer.check_missing_values()
    print(f"   Total missing values: {missing.sum()}\n")

    # Step 5: Visualization
    print("5. Visualization: Creating charts...")
    plotter = Plotter()

    # Create multiple plots
    try:
        # Correlation heatmap (if numeric data available)
        fig1 = plt.figure(figsize=(10, 8))
        analyzer.plot_correlation_heatmap()
        plotter.save_plot(fig1, 'workflow_correlation.png')

        # Box plot
        fig2 = plt.figure(figsize=(12, 6))
        analyzer.plot_boxplot()
        plotter.save_plot(fig2, 'workflow_boxplot.png')

        print("   Charts saved: correlation heatmap and box plot\n")

    except Exception as e:
        print(f"   Visualization error: {e}\n")

    # Step 6: Export Results
    print("6. Export: Saving processed data...")
    processor.save_csv('processed_companies_data.csv')
    print("   Data exported to 'processed_companies_data.csv'\n")

    print("=== Workflow Complete ===")
    print("Generated files:")
    print("- processed_companies_data.csv")
    print("- workflow_correlation.png")
    print("- workflow_boxplot.png")
    print("\nCheck examples/ directory for more specific demonstrations!")

if __name__ == "__main__":
    main()
