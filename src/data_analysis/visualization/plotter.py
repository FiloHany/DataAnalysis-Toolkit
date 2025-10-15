"""
Visualization utilities using Strategy pattern for different plot types.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Any, Optional, Tuple
from ..config import logger, PLOT_STYLE, FIGURE_SIZE


class PlotStrategy:
    """Base class for plotting strategies."""

    def plot(self, data: pd.DataFrame, **kwargs) -> plt.Figure:
        """Create plot."""
        pass


class LinePlotStrategy(PlotStrategy):
    """Strategy for line plots."""

    def plot(self, data: pd.DataFrame, **kwargs) -> plt.Figure:
        x = kwargs.get('x')
        y = kwargs.get('y')
        title = kwargs.get('title', 'Line Plot')
        figsize = kwargs.get('figsize', FIGURE_SIZE)

        fig, ax = plt.subplots(figsize=figsize)
        if x and y:
            ax.plot(data[x], data[y])
        else:
            data.plot(ax=ax)
        ax.set_title(title)
        ax.set_xlabel(x or 'X')
        ax.set_ylabel(y or 'Y')
        plt.tight_layout()
        return fig


class BarPlotStrategy(PlotStrategy):
    """Strategy for bar plots."""

    def plot(self, data: pd.DataFrame, **kwargs) -> plt.Figure:
        x = kwargs.get('x')
        y = kwargs.get('y')
        title = kwargs.get('title', 'Bar Plot')
        figsize = kwargs.get('figsize', FIGURE_SIZE)

        fig, ax = plt.subplots(figsize=figsize)
        if x and y:
            ax.bar(data[x], data[y])
        else:
            data.plot(kind='bar', ax=ax)
        ax.set_title(title)
        ax.set_xlabel(x or 'X')
        ax.set_ylabel(y or 'Y')
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig


class ScatterPlotStrategy(PlotStrategy):
    """Strategy for scatter plots."""

    def plot(self, data: pd.DataFrame, **kwargs) -> plt.Figure:
        x = kwargs.get('x')
        y = kwargs.get('y')
        s = kwargs.get('s', 50)
        c = kwargs.get('c', 'blue')
        title = kwargs.get('title', 'Scatter Plot')
        figsize = kwargs.get('figsize', FIGURE_SIZE)

        fig, ax = plt.subplots(figsize=figsize)
        ax.scatter(data[x], data[y], s=s, c=c)
        ax.set_title(title)
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        plt.tight_layout()
        return fig


class HistogramStrategy(PlotStrategy):
    """Strategy for histograms."""

    def plot(self, data: pd.DataFrame, **kwargs) -> plt.Figure:
        column = kwargs.get('column')
        bins = kwargs.get('bins', 20)
        title = kwargs.get('title', f'Histogram of {column}')
        figsize = kwargs.get('figsize', FIGURE_SIZE)

        fig, ax = plt.subplots(figsize=figsize)
        ax.hist(data[column].dropna(), bins=bins, edgecolor='black')
        ax.set_title(title)
        ax.set_xlabel(column)
        ax.set_ylabel('Frequency')
        plt.tight_layout()
        return fig


class BoxPlotStrategy(PlotStrategy):
    """Strategy for box plots."""

    def plot(self, data: pd.DataFrame, **kwargs) -> plt.Figure:
        title = kwargs.get('title', 'Box Plot')
        figsize = kwargs.get('figsize', FIGURE_SIZE)

        fig, ax = plt.subplots(figsize=figsize)
        data.boxplot(ax=ax)
        ax.set_title(title)
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig


class PieChartStrategy(PlotStrategy):
    """Strategy for pie charts."""

    def plot(self, data: pd.DataFrame, **kwargs) -> plt.Figure:
        y = kwargs.get('y')
        title = kwargs.get('title', 'Pie Chart')
        figsize = kwargs.get('figsize', FIGURE_SIZE)

        fig, ax = plt.subplots(figsize=figsize)
        ax.pie(data[y], labels=data.index, autopct='%1.1f%%')
        ax.set_title(title)
        plt.tight_layout()
        return fig


class AreaPlotStrategy(PlotStrategy):
    """Strategy for area plots."""

    def plot(self, data: pd.DataFrame, **kwargs) -> plt.Figure:
        title = kwargs.get('title', 'Area Plot')
        figsize = kwargs.get('figsize', FIGURE_SIZE)

        fig, ax = plt.subplots(figsize=figsize)
        data.plot.area(ax=ax)
        ax.set_title(title)
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig


class Plotter:
    """
    Plotter class using Strategy pattern for different visualization types.
    Provides unified interface for creating various plots.
    """

    def __init__(self):
        """Initialize plotter with available strategies."""
        self.strategies = {
            'line': LinePlotStrategy(),
            'bar': BarPlotStrategy(),
            'scatter': ScatterPlotStrategy(),
            'histogram': HistogramStrategy(),
            'box': BoxPlotStrategy(),
            'pie': PieChartStrategy(),
            'area': AreaPlotStrategy()
        }
        # Set default style
        plt.style.use(PLOT_STYLE)

    def create_plot(self, plot_type: str, data: pd.DataFrame, **kwargs) -> plt.Figure:
        """
        Create a plot using specified strategy.

        Args:
            plot_type: Type of plot ('line', 'bar', 'scatter', etc.)
            data: DataFrame to plot
            **kwargs: Plot-specific parameters

        Returns:
            Matplotlib Figure object

        Raises:
            ValueError: If plot type not supported
        """
        if plot_type not in self.strategies:
            available = list(self.strategies.keys())
            raise ValueError(f"Plot type '{plot_type}' not supported. Available: {available}")

        strategy = self.strategies[plot_type]
        fig = strategy.plot(data, **kwargs)
        logger.info(f"Created {plot_type} plot")
        return fig

    def show_plot(self, fig: plt.Figure):
        """Display the plot."""
        plt.show()

    def save_plot(self, fig: plt.Figure, filename: str, dpi: int = 300):
        """
        Save plot to file.

        Args:
            fig: Figure to save
            filename: Output filename
            dpi: Resolution
        """
        fig.savefig(filename, dpi=dpi, bbox_inches='tight')
        logger.info(f"Saved plot to {filename}")

    # Convenience methods for common plots
    def line_plot(self, data: pd.DataFrame, x: str, y: str, title: str = 'Line Plot',
                  figsize: Tuple[int, int] = FIGURE_SIZE) -> plt.Figure:
        """Create line plot."""
        return self.create_plot('line', data, x=x, y=y, title=title, figsize=figsize)

    def bar_plot(self, data: pd.DataFrame, x: str = None, y: str = None,
                 title: str = 'Bar Plot', figsize: Tuple[int, int] = FIGURE_SIZE) -> plt.Figure:
        """Create bar plot."""
        return self.create_plot('bar', data, x=x, y=y, title=title, figsize=figsize)

    def scatter_plot(self, data: pd.DataFrame, x: str, y: str, s: int = 50, c: str = 'blue',
                     title: str = 'Scatter Plot', figsize: Tuple[int, int] = FIGURE_SIZE) -> plt.Figure:
        """Create scatter plot."""
        return self.create_plot('scatter', data, x=x, y=y, s=s, c=c, title=title, figsize=figsize)

    def histogram(self, data: pd.DataFrame, column: str, bins: int = 20,
                  title: str = None, figsize: Tuple[int, int] = FIGURE_SIZE) -> plt.Figure:
        """Create histogram."""
        if title is None:
            title = f'Histogram of {column}'
        return self.create_plot('histogram', data, column=column, bins=bins, title=title, figsize=figsize)

    def box_plot(self, data: pd.DataFrame, title: str = 'Box Plot',
                 figsize: Tuple[int, int] = FIGURE_SIZE) -> plt.Figure:
        """Create box plot."""
        return self.create_plot('box', data, title=title, figsize=figsize)

    def pie_chart(self, data: pd.DataFrame, y: str, title: str = 'Pie Chart',
                  figsize: Tuple[int, int] = FIGURE_SIZE) -> plt.Figure:
        """Create pie chart."""
        return self.create_plot('pie', data, y=y, title=title, figsize=figsize)

    def area_plot(self, data: pd.DataFrame, title: str = 'Area Plot',
                  figsize: Tuple[int, int] = FIGURE_SIZE) -> plt.Figure:
        """Create area plot."""
        return self.create_plot('area', data, title=title, figsize=figsize)
