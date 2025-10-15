"""
Example: Visualization gallery
Demonstrates various plot types using the visualization module.
"""

import pandas as pd
import numpy as np
from src.data_analysis.visualization import Plotter
import matplotlib.pyplot as plt

def create_sample_data():
    """Create sample data for visualization."""
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', periods=50, freq='D')

    data = {
        'Date': dates,
        'Sales': np.random.normal(1000, 200, 50),
        'Profit': np.random.normal(200, 50, 50),
        'Customers': np.random.randint(50, 150, 50),
        'Category': np.random.choice(['A', 'B', 'C', 'D'], 50),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], 50)
    }
    return pd.DataFrame(data)

def main():
    # Create sample data
    df = create_sample_data()
    df.set_index('Date', inplace=True)

    # Initialize plotter
    plotter = Plotter()

    # 1. Line plot
    fig1 = plotter.line_plot(df, x=df.index, y='Sales', title='Sales Over Time')
    plotter.save_plot(fig1, 'line_plot.png')

    # 2. Bar plot
    monthly_sales = df.resample('W').sum()
    fig2 = plotter.bar_plot(monthly_sales, y='Sales', title='Weekly Sales')
    plotter.save_plot(fig2, 'bar_plot.png')

    # 3. Scatter plot
    fig3 = plotter.scatter_plot(df, x='Sales', y='Profit', title='Sales vs Profit')
    plotter.save_plot(fig3, 'scatter_plot.png')

    # 4. Histogram
    fig4 = plotter.histogram(df, column='Customers', bins=15, title='Customer Distribution')
    plotter.save_plot(fig4, 'histogram.png')

    # 5. Box plot
    fig5 = plotter.box_plot(df[['Sales', 'Profit', 'Customers']], title='Distribution Analysis')
    plotter.save_plot(fig5, 'box_plot.png')

    # 6. Area plot
    fig6 = plotter.area_plot(df[['Sales', 'Profit']], title='Sales and Profit Trends')
    plotter.save_plot(fig6, 'area_plot.png')

    # 7. Pie chart (using category counts)
    category_counts = df['Category'].value_counts()
    fig7 = plotter.pie_chart(pd.DataFrame({'Count': category_counts}), y='Count', title='Category Distribution')
    plotter.save_plot(fig7, 'pie_chart.png')

    print("All visualization examples saved as PNG files:")
    print("- line_plot.png")
    print("- bar_plot.png")
    print("- scatter_plot.png")
    print("- histogram.png")
    print("- box_plot.png")
    print("- area_plot.png")
    print("- pie_chart.png")

if __name__ == "__main__":
    main()
