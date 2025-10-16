# Data Analysis Toolkit

A professional, modular data analysis toolkit built with SOLID principles and design patterns. This package provides comprehensive tools for web scraping, data processing, cleaning, exploratory data analysis, API interactions, and visualization.

## Features

- **Modular Architecture**: Clean separation of concerns with dedicated modules
- **SOLID Principles**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **Design Patterns**: Strategy pattern for flexible operations, Factory pattern for object creation
- **Web Scraping**: Extract data from websites using BeautifulSoup
- **Data Processing**: Flexible pandas operations with Strategy pattern
- **Data Cleaning**: Comprehensive cleaning utilities
- **EDA**: Exploratory data analysis with statistical and visual methods
- **API Integration**: Cryptocurrency data from CoinMarketCap API
- **Visualization**: Multiple plot types with consistent interface
- **Professional Logging**: Comprehensive logging throughout the application

## Installation

### From Source
```bash
git clone https://github.com/yourusername/data-analysis-toolkit.git
cd data-analysis-toolkit
pip install -r requirements.txt
pip install -e .
```

### From PyPI (when published)
```bash
pip install data-analysis-toolkit
```

## Quick Start

```python
from src.data_analysis import scrapers, processors, cleaners, eda, api, visualization

# Web scraping
scraper = scrapers.WebScraper()
companies_df = scraper.scrape_companies_list('https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue')

# Data processing
processor = processors.PandasProcessor()
processor.set_data(companies_df)
filtered_data = processor.filter_data("Rank <= 10")

# Data cleaning
cleaner = cleaners.DataCleaner(filtered_data)
clean_data = cleaner.remove_duplicates().get_data()

# EDA
analyzer = eda.EDAAnalyzer(clean_data)
summary = analyzer.get_summary_statistics()
analyzer.plot_correlation_heatmap()

# API data collection
crypto_api = api.CryptoAPI(api_key='your-api-key')
crypto_data = crypto_api.get_listings(limit=50)

# Visualization
plotter = visualization.Plotter()
fig = plotter.scatter_plot(crypto_data, x='quote.USD.price', y='quote.USD.volume_24h')
plotter.show_plot(fig)
```

## Project Structure

```
src/data_analysis/
├── __init__.py          # Package initialization
├── config.py            # Configuration settings
├── scrapers/            # Web scraping module
│   ├── __init__.py
│   └── web_scraper.py
├── processors/          # Data processing module
│   ├── __init__.py
│   ├── base_processor.py
│   └── pandas_processor.py
├── cleaners/            # Data cleaning module
│   ├── __init__.py
│   └── data_cleaner.py
├── eda/                 # Exploratory analysis module
│   ├── __init__.py
│   └── exploratory_analysis.py
├── api/                 # API interaction module
│   ├── __init__.py
│   └── crypto_api.py
└── visualization/       # Visualization module
    ├── __init__.py
    └── plotter.py
```

## Architecture Principles

### SOLID Principles Implementation

1. **Single Responsibility**: Each class has one primary responsibility
   - `WebScraper`: Handles only web scraping
   - `DataCleaner`: Handles only data cleaning operations
   - `EDAAnalyzer`: Handles only exploratory analysis

2. **Open/Closed**: Classes are open for extension, closed for modification
   - Strategy pattern allows adding new operations without modifying existing code
   - New plot types can be added via new strategies

3. **Liskov Substitution**: Subtypes are substitutable for their base types
   - All strategy classes implement the same interface

4. **Interface Segregation**: Clients depend only on methods they use
   - Separate interfaces for different operations

5. **Dependency Inversion**: High-level modules don't depend on low-level modules
   - Abstract base classes define interfaces
   - Concrete implementations can be swapped

### Design Patterns Used

- **Strategy Pattern**: For flexible data operations and plotting
- **Factory Pattern**: For creating different types of processors
- **Template Method**: For consistent API request handling

## Modules Overview

### Scrapers
Extract data from web sources with error handling and logging.

### Processors
Flexible data manipulation using Strategy pattern for operations like filtering, sorting, grouping, and merging.

### Cleaners
Comprehensive data cleaning utilities for duplicates, formatting, missing values, and text processing.

### EDA
Statistical analysis and visualization for exploratory data analysis.

### API
Professional API client for cryptocurrency data with rate limiting and automated collection.

### Visualization
Unified plotting interface supporting multiple chart types.

## Configuration

Set environment variables:
```bash
export CMC_API_KEY="your-coinmarketcap-api-key"
```

Or create a `.env` file:
```
CMC_API_KEY=your-coinmarketcap-api-key
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Quality
```bash
black src/
flake8 src/
mypy src/
```

## Examples

See the `examples/` directory for complete usage examples including:
- Web scraping companies data
- Data cleaning pipeline
- Exploratory analysis
- Crypto API automation
- Visualization gallery

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Contact

feloh64@gmail.com

https://github.com/FiloHany/DataAnalysis-Toolkit.git
