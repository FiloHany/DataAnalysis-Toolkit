"""
Pandas-specific data processing strategies.
Implements various data manipulation operations using Strategy pattern.
"""

import pandas as pd
from typing import List, Dict, Any, Optional, Union
from .base_processor import DataOperationStrategy
from ..config import logger


class FilterStrategy(DataOperationStrategy):
    """Strategy for filtering data."""

    def execute(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        condition = kwargs.get('condition')
        if condition is None:
            raise ValueError("Filter condition required")

        if isinstance(condition, str):
            # Evaluate string condition
            result = data.query(condition)
        else:
            # Apply boolean mask
            result = data[condition]

        logger.info(f"Filtered data from {len(data)} to {len(result)} rows")
        return result


class SortStrategy(DataOperationStrategy):
    """Strategy for sorting data."""

    def execute(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        by = kwargs.get('by')
        ascending = kwargs.get('ascending', True)

        if by is None:
            raise ValueError("Sort column(s) required")

        result = data.sort_values(by=by, ascending=ascending)
        logger.info(f"Sorted data by {by}")
        return result


class GroupByStrategy(DataOperationStrategy):
    """Strategy for groupby operations."""

    def execute(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        by = kwargs.get('by')
        agg_funcs = kwargs.get('agg_funcs', {})

        if by is None:
            raise ValueError("Groupby column(s) required")

        grouped = data.groupby(by)

        if agg_funcs:
            result = grouped.agg(agg_funcs)
        else:
            result = grouped.size().reset_index(name='count')

        logger.info(f"Grouped data by {by}")
        return result


class IndexStrategy(DataOperationStrategy):
    """Strategy for indexing operations."""

    def execute(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        column = kwargs.get('column')
        operation = kwargs.get('operation', 'set_index')

        if column is None:
            raise ValueError("Column name required for indexing")

        if operation == 'set_index':
            result = data.set_index(column)
            logger.info(f"Set {column} as index")
        elif operation == 'reset_index':
            result = data.reset_index()
            logger.info("Reset index")
        else:
            raise ValueError(f"Unknown indexing operation: {operation}")

        return result


class MergeStrategy(DataOperationStrategy):
    """Strategy for merging DataFrames."""

    def execute(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        other_df = kwargs.get('other')
        how = kwargs.get('how', 'inner')
        on = kwargs.get('on')

        if other_df is None:
            raise ValueError("Other DataFrame required for merge")

        result = data.merge(other_df, how=how, on=on)
        logger.info(f"Merged DataFrames with {how} join")
        return result


class PandasProcessor:
    """
    Pandas processor with pre-configured strategies.
    Extends base processor with pandas-specific operations.
    """

    def __init__(self):
        """Initialize with common pandas strategies."""
        from .base_processor import DataProcessor
        self.processor = DataProcessor()

        # Add strategies
        self.processor.add_strategy('filter', FilterStrategy())
        self.processor.add_strategy('sort', SortStrategy())
        self.processor.add_strategy('groupby', GroupByStrategy())
        self.processor.add_strategy('index', IndexStrategy())
        self.processor.add_strategy('merge', MergeStrategy())

    def set_data(self, data: pd.DataFrame):
        """Set data for processing."""
        self.processor.set_data(data)

    def get_data(self) -> Optional[pd.DataFrame]:
        """Get current data."""
        return self.processor.get_data()

    def filter_data(self, condition: Union[str, pd.Series]) -> pd.DataFrame:
        """Filter data using condition."""
        return self.processor.execute_operation('filter', condition=condition)

    def sort_data(self, by: Union[str, List[str]], ascending: bool = True) -> pd.DataFrame:
        """Sort data by column(s)."""
        return self.processor.execute_operation('sort', by=by, ascending=ascending)

    def groupby_data(self, by: Union[str, List[str]], agg_funcs: Optional[Dict] = None) -> pd.DataFrame:
        """Group data and apply aggregations."""
        return self.processor.execute_operation('groupby', by=by, agg_funcs=agg_funcs)

    def set_index(self, column: str) -> pd.DataFrame:
        """Set column as index."""
        return self.processor.execute_operation('index', column=column, operation='set_index')

    def reset_index(self) -> pd.DataFrame:
        """Reset index."""
        return self.processor.execute_operation('index', operation='reset_index')

    def merge_data(self, other: pd.DataFrame, how: str = 'inner', on: Optional[Union[str, List[str]]] = None) -> pd.DataFrame:
        """Merge with another DataFrame."""
        return self.processor.execute_operation('merge', other=other, how=how, on=on)

    def load_csv(self, file_path: str, **kwargs) -> pd.DataFrame:
        """Load CSV file."""
        return self.processor.load_csv(file_path, **kwargs)

    def save_csv(self, file_path: str, **kwargs):
        """Save to CSV file."""
        self.processor.save_csv(file_path, **kwargs)
