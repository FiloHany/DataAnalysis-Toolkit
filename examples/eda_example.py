"""
Example: Exploratory Data Analysis
Demonstrates the EDA module usage.
"""

import pandas as pd
import numpy as np
from src.data_analysis.eda import EDAAnalyzer
from src.data_analysis.visualization import Plotter

def create_sample_data():
    """Create sample data for EDA demonstration."""
    np.random.seed(42)
    data = {
        'Feature1': np.random.normal(50, 10, 100),
        'Feature2': np.random.normal(30, 5, 100),
        'Feature3': np.random.normal(70, 15, 100),
        'Category': np.random.choice(['A', 'B', 'C'], 100),
        'Target': np.random.randint(0, 2, 100)
    }
    return pd.DataFrame(data)

def main():
    # Create sample data
    df = create_sample_data()

    # Initialize EDA analyzer
    analyzer = EDAAnalyzer(df)

    # Basic statistics
    print("Summary Statistics:")
    print(analyzer.get_summary_statistics())

    # Missing values check
    print("\nMissing Values:")
    print(analyzer.check_missing_values())

    # Unique counts
    print("\nUnique Value Counts:")
    print(analyzer.get_unique_counts())

    # Correlation analysis
    print("\nCorrelation Matrix:")
    corr = analyzer.analyze_correlations()
    print(corr)

    # Create visualizations
    plotter = Plotter()

    # Correlation heatmap
    fig1 = plt.figure()  # Need to import matplotlib
    analyzer.plot_correlation_heatmap()
    plotter.save_plot(fig1, 'correlation_heatmap.png')

    # Box plot
    fig2 = plt.figure()
    analyzer.plot_boxplot()
    plotter.save_plot(fig2, 'boxplot.png')

    # Histogram
    fig3 = plt.figure()
    analyzer.plot_histogram('Feature1', bins=20)
    plotter.save_plot(fig3, 'histogram.png')

    print("\nEDA visualizations saved as PNG files")

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    main()
