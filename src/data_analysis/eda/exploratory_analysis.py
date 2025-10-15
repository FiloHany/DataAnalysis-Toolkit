"""
Exploratory Data Analysis utilities with Strategy pattern.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Any, Optional, Tuple
from ..config import logger, PLOT_STYLE, FIGURE_SIZE


class AnalysisStrategy:
    """Base class for analysis strategies."""

    def execute(self, data: pd.DataFrame, **kwargs) -> Any:
        """Execute analysis."""
        pass


class SummaryStatisticsStrategy(AnalysisStrategy):
    """Strategy for summary statistics."""

    def execute(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        numeric_only = kwargs.get('numeric_only', True)
        return data.describe() if numeric_only else data.describe(include='all')


class CorrelationAnalysisStrategy(AnalysisStrategy):
    """Strategy for correlation analysis."""

    def execute(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        numeric_only = kwargs.get('numeric_only', True)
        method = kwargs.get('method', 'pearson')
        return data.corr(numeric_only=numeric_only, method=method)


class GroupAnalysisStrategy(AnalysisStrategy):
    """Strategy for group-based analysis."""

    def execute(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        groupby_col = kwargs.get('groupby_col')
        agg_funcs = kwargs.get('agg_funcs', 'mean')
        numeric_only = kwargs.get('numeric_only', True)

        if groupby_col is None:
            raise ValueError("groupby_col required")

        grouped = data.groupby(groupby_col)
        if isinstance(agg_funcs, str):
            return grouped.agg(agg_funcs, numeric_only=numeric_only)
        else:
            return grouped.agg(agg_funcs)


class EDAAnalyzer:
    """
    Exploratory Data Analysis analyzer using Strategy pattern.
    Provides various analysis methods with visualization capabilities.
    """

    def __init__(self, data: Optional[pd.DataFrame] = None):
        """
        Initialize EDA analyzer.

        Args:
            data: DataFrame for analysis
        """
        self.data = data.copy() if data is not None else None
        self.strategies = {
            'summary': SummaryStatisticsStrategy(),
            'correlation': CorrelationAnalysisStrategy(),
            'group_analysis': GroupAnalysisStrategy()
        }
        # Set default plot style
        plt.style.use(PLOT_STYLE)

    def set_data(self, data: pd.DataFrame):
        """Set data for analysis."""
        self.data = data.copy()
        logger.info(f"Data set for EDA with shape: {data.shape}")

    def get_data(self) -> Optional[pd.DataFrame]:
        """Get current data."""
        return self.data

    def get_summary_statistics(self, numeric_only: bool = True) -> pd.DataFrame:
        """
        Get summary statistics of the data.

        Args:
            numeric_only: Include only numeric columns

        Returns:
            Summary statistics DataFrame
        """
        if self.data is None:
            raise ValueError("No data set for analysis")

        result = self.strategies['summary'].execute(self.data, numeric_only=numeric_only)
        logger.info("Generated summary statistics")
        return result

    def analyze_correlations(self, numeric_only: bool = True, method: str = 'pearson') -> pd.DataFrame:
        """
        Analyze correlations between variables.

        Args:
            numeric_only: Include only numeric columns
            method: Correlation method ('pearson', 'spearman', 'kendall')

        Returns:
            Correlation matrix
        """
        if self.data is None:
            raise ValueError("No data set for analysis")

        result = self.strategies['correlation'].execute(self.data,
                                                       numeric_only=numeric_only,
                                                       method=method)
        logger.info(f"Generated {method} correlation matrix")
        return result

    def plot_correlation_heatmap(self, figsize: Tuple[int, int] = FIGURE_SIZE):
        """
        Plot correlation heatmap.

        Args:
            figsize: Figure size
        """
        if self.data is None:
            raise ValueError("No data set for analysis")

        corr_matrix = self.analyze_correlations()
        plt.figure(figsize=figsize)
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title('Correlation Heatmap')
        plt.tight_layout()
        logger.info("Plotted correlation heatmap")

    def group_analysis(self, groupby_col: str, agg_funcs: Any = 'mean',
                      numeric_only: bool = True) -> pd.DataFrame:
        """
        Perform group-based analysis.

        Args:
            groupby_col: Column to group by
            agg_funcs: Aggregation functions
            numeric_only: Include only numeric columns

        Returns:
            Grouped analysis results
        """
        if self.data is None:
            raise ValueError("No data set for analysis")

        result = self.strategies['group_analysis'].execute(self.data,
                                                          groupby_col=groupby_col,
                                                          agg_funcs=agg_funcs,
                                                          numeric_only=numeric_only)
        logger.info(f"Performed group analysis by {groupby_col}")
        return result

    def plot_boxplot(self, figsize: Tuple[int, int] = FIGURE_SIZE):
        """
        Plot boxplot for numeric columns.

        Args:
            figsize: Figure size
        """
        if self.data is None:
            raise ValueError("No data set for analysis")

        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            logger.warning("No numeric columns found for boxplot")
            return

        plt.figure(figsize=figsize)
        self.data[numeric_cols].boxplot()
        plt.title('Boxplot of Numeric Variables')
        plt.xticks(rotation=45)
        plt.tight_layout()
        logger.info("Plotted boxplot")

    def plot_histogram(self, column: str, bins: int = 20, figsize: Tuple[int, int] = FIGURE_SIZE):
        """
        Plot histogram for a specific column.

        Args:
            column: Column name
            bins: Number of bins
            figsize: Figure size
        """
        if self.data is None:
            raise ValueError("No data set for analysis")

        if column not in self.data.columns:
            raise ValueError(f"Column {column} not found")

        plt.figure(figsize=figsize)
        plt.hist(self.data[column].dropna(), bins=bins, edgecolor='black')
        plt.title(f'Histogram of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.tight_layout()
        logger.info(f"Plotted histogram for {column}")

    def check_missing_values(self) -> pd.Series:
        """
        Check for missing values in each column.

        Returns:
            Series with missing value counts
        """
        if self.data is None:
            raise ValueError("No data set for analysis")

        missing = self.data.isnull().sum()
        logger.info(f"Checked missing values: {missing.sum()} total missing")
        return missing

    def get_unique_counts(self) -> pd.Series:
        """
        Get unique value counts for each column.

        Returns:
            Series with unique counts
        """
        if self.data is None:
            raise ValueError("No data set for analysis")

        unique_counts = self.data.nunique()
        logger.info("Calculated unique value counts")
        return unique_counts

    def analyze_top_values(self, column: str, n: int = 10) -> pd.Series:
        """
        Analyze top N most frequent values in a column.

        Args:
            column: Column name
            n: Number of top values

        Returns:
            Series with top values and counts
        """
        if self.data is None:
            raise ValueError("No data set for analysis")

        if column not in self.data.columns:
            raise ValueError(f"Column {column} not found")

        top_values = self.data[column].value_counts().head(n)
        logger.info(f"Analyzed top {n} values in {column}")
        return top_values
