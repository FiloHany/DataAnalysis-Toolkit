"""
Example: Cryptocurrency API data collection
Demonstrates the API module usage.
Note: Requires valid CoinMarketCap API key
"""

import os
from src.data_analysis.api import CryptoAPI
from src.data_analysis.visualization import Plotter
import matplotlib.pyplot as plt

def main():
    # Check for API key
    api_key = os.getenv('CMC_API_KEY')
    if not api_key:
        print("Please set CMC_API_KEY environment variable with your CoinMarketCap API key")
        return

    # Initialize API client
    crypto_api = CryptoAPI(api_key=api_key)

    # Get current listings
    print("Fetching cryptocurrency listings...")
    crypto_df = crypto_api.get_listings(limit=20)
    print(f"Retrieved {len(crypto_df)} cryptocurrencies")
    print(crypto_df[['name', 'symbol', 'quote.USD.price']].head())

    # Clean the data
    cleaned_df = crypto_api.clean_crypto_data(crypto_df)
    print(f"Cleaned data has {len(cleaned_df)} records")

    # Calculate price changes
    price_changes = crypto_api.calculate_price_changes(cleaned_df)
    print("\nPrice change statistics:")
    print(price_changes.head())

    # Get Bitcoin data for time series
    bitcoin_data = crypto_api.get_bitcoin_data(cleaned_df)
    if not bitcoin_data.empty:
        print(f"\nBitcoin data points: {len(bitcoin_data)}")

        # Create visualization
        plotter = Plotter()
        fig = plotter.line_plot(bitcoin_data, x='timestamp', y='quote.USD.price',
                               title='Bitcoin Price Over Time')
        plotter.save_plot(fig, 'bitcoin_price.png')
        print("Bitcoin price chart saved as 'bitcoin_price.png'")

    # Optional: Run automated collection (commented out to avoid long execution)
    # print("\nStarting automated collection (this will take time)...")
    # all_data = crypto_api.run_automated_collection(cycles=5, interval=10, output_file='crypto_history.csv')
    # print(f"Collected {len(all_data)} total records")

if __name__ == "__main__":
    main()
