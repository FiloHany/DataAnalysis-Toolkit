"""
Base processor with Strategy pattern for data operations.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
import pandas as pd
from ..config import logger


class DataOperationStrategy(ABC):
    """Abstract base class for data operation strategies."""

    @abstractmethod
    def execute(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """Execute the data operation."""
        pass


class DataProcessor:
    """
    Data processor using Strategy pattern for flexible operations.
    Follows Single Responsibility Principle and Open/Closed Principle.
    """

    def __init__(self):
        """Initialize processor with available strategies."""
        self.strategies: Dict[str, DataOperationStrategy] = {}
        self._data: Optional[pd.DataFrame] = None

    def add_strategy(self, name: str, strategy: DataOperationStrategy):
        """
        Add a new operation strategy.

        Args:
            name: Strategy name
            strategy: Strategy instance
        """
        self.strategies[name] = strategy
        logger.info(f"Added strategy: {name}")

    def set_data(self, data: pd.DataFrame):
        """
        Set the data to process.

        Args:
            data: DataFrame to process
        """
        self._data = data.copy()
        logger.info(f"Data set with shape: {data.shape}")

    def get_data(self) -> Optional[pd.DataFrame]:
        """Get current data."""
        return self._data

    def execute_operation(self, strategy_name: str, **kwargs) -> pd.DataFrame:
        """
        Execute a data operation using specified strategy.

        Args:
            strategy_name: Name of strategy to use
            **kwargs: Arguments for the strategy

        Returns:
            Processed DataFrame

        Raises:
            ValueError: If strategy not found or no data set
        """
        if self._data is None:
            raise ValueError("No data set. Use set_data() first.")

        if strategy_name not in self.strategies:
            available = list(self.strategies.keys())
            raise ValueError(f"Strategy '{strategy_name}' not found. Available: {available}")

        strategy = self.strategies[strategy_name]
        logger.info(f"Executing strategy: {strategy_name}")
        result = strategy.execute(self._data, **kwargs)
        self._data = result  # Update internal data
        return result

    def load_csv(self, file_path: str, **kwargs) -> pd.DataFrame:
        """
        Load data from CSV file.

        Args:
            file_path: Path to CSV file
            **kwargs: Additional pandas read_csv arguments

        Returns:
            Loaded DataFrame
        """
        try:
            df = pd.read_csv(file_path, **kwargs)
            self.set_data(df)
            logger.info(f"Loaded CSV from {file_path} with shape {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Failed to load CSV {file_path}: {e}")
            raise

    def save_csv(self, file_path: str, **kwargs):
        """
        Save current data to CSV file.

        Args:
            file_path: Path to save CSV
            **kwargs: Additional pandas to_csv arguments
        """
        if self._data is None:
            raise ValueError("No data to save. Use set_data() first.")

        try:
            self._data.to_csv(file_path, **kwargs)
            logger.info(f"Saved data to {file_path}")
        except Exception as e:
            logger.error(f"Failed to save CSV {file_path}: {e}")
            raise
