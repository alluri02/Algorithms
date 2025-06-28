"""
Data loader for various data sources in the segmentation pipeline.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, Union, List
import logging
import json

logger = logging.getLogger(__name__)


class DataLoader:
    """Load data from various sources for the segmentation pipeline."""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the data loader.
        
        Args:
            data_dir: Directory containing data files
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def load_csv(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """
        Load data from CSV file.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            Loaded DataFrame
        """
        try:
            file_path = Path(file_path)
            logger.info(f"Loading CSV data from {file_path}")
            
            data = pd.read_csv(file_path)
            logger.info(f"Loaded {len(data)} records with {len(data.columns)} features")
            
            return data
            
        except Exception as e:
            logger.error(f"Error loading CSV file {file_path}: {str(e)}")
            raise
    
    def load_parquet(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """
        Load data from Parquet file.
        
        Args:
            file_path: Path to Parquet file
            
        Returns:
            Loaded DataFrame
        """
        try:
            file_path = Path(file_path)
            logger.info(f"Loading Parquet data from {file_path}")
            
            data = pd.read_parquet(file_path)
            logger.info(f"Loaded {len(data)} records with {len(data.columns)} features")
            
            return data
            
        except Exception as e:
            logger.error(f"Error loading Parquet file {file_path}: {str(e)}")
            raise
    
    def load_json(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """
        Load data from JSON file.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Loaded DataFrame
        """
        try:
            file_path = Path(file_path)
            logger.info(f"Loading JSON data from {file_path}")
            
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Convert to DataFrame
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                df = pd.DataFrame([data])
            else:
                raise ValueError("JSON data must be a list or dictionary")
            
            logger.info(f"Loaded {len(df)} records with {len(df.columns)} features")
            
            return df
            
        except Exception as e:
            logger.error(f"Error loading JSON file {file_path}: {str(e)}")
            raise
    
    def load_from_database(self, 
                          connection_string: str,
                          query: str) -> pd.DataFrame:
        """
        Load data from database using SQL query.
        
        Args:
            connection_string: Database connection string
            query: SQL query to execute
            
        Returns:
            Query results as DataFrame
        """
        try:
            import sqlalchemy as sa
            
            logger.info(f"Connecting to database and executing query")
            
            engine = sa.create_engine(connection_string)
            data = pd.read_sql(query, engine)
            
            logger.info(f"Loaded {len(data)} records with {len(data.columns)} features from database")
            
            return data
            
        except ImportError:
            logger.error("SQLAlchemy not installed. Please install it to use database functionality.")
            raise
        except Exception as e:
            logger.error(f"Error loading data from database: {str(e)}")
            raise
    
    def load_from_api(self, 
                     url: str,
                     headers: Optional[Dict[str, str]] = None,
                     params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        Load data from REST API.
        
        Args:
            url: API endpoint URL
            headers: Request headers
            params: Query parameters
            
        Returns:
            API response data as DataFrame
        """
        try:
            import requests
            
            logger.info(f"Fetching data from API: {url}")
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Convert to DataFrame
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                # Handle nested JSON structures
                if 'data' in data:
                    df = pd.DataFrame(data['data'])
                elif 'results' in data:
                    df = pd.DataFrame(data['results'])
                else:
                    df = pd.DataFrame([data])
            else:
                raise ValueError("API response must be JSON format")
            
            logger.info(f"Loaded {len(df)} records with {len(df.columns)} features from API")
            
            return df
            
        except ImportError:
            logger.error("Requests library not installed. Please install it to use API functionality.")
            raise
        except Exception as e:
            logger.error(f"Error loading data from API: {str(e)}")
            raise
    
    def save_data(self, 
                  data: pd.DataFrame,
                  file_path: Union[str, Path],
                  format: str = 'csv') -> None:
        """
        Save DataFrame to file.
        
        Args:
            data: DataFrame to save
            file_path: Output file path
            format: File format ('csv', 'parquet', 'json')
        """
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"Saving data to {file_path} in {format} format")
            
            if format.lower() == 'csv':
                data.to_csv(file_path, index=False)
            elif format.lower() == 'parquet':
                data.to_parquet(file_path, index=False)
            elif format.lower() == 'json':
                data.to_json(file_path, orient='records', indent=2)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            logger.info(f"Data saved successfully to {file_path}")
            
        except Exception as e:
            logger.error(f"Error saving data to {file_path}: {str(e)}")
            raise
    
    def get_data_info(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Get comprehensive information about the dataset.
        
        Args:
            data: Input DataFrame
            
        Returns:
            Dictionary with dataset information
        """
        info = {
            'shape': data.shape,
            'columns': list(data.columns),
            'dtypes': data.dtypes.to_dict(),
            'missing_values': data.isnull().sum().to_dict(),
            'memory_usage': data.memory_usage(deep=True).sum(),
            'duplicate_rows': data.duplicated().sum()
        }
        
        # Add statistics for numerical columns
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            info['numeric_statistics'] = data[numeric_cols].describe().to_dict()
        
        # Add value counts for categorical columns
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) > 0:
            info['categorical_statistics'] = {}
            for col in categorical_cols:
                info['categorical_statistics'][col] = data[col].value_counts().to_dict()
        
        return info
    
    def validate_data(self, 
                     data: pd.DataFrame,
                     required_columns: Optional[List[str]] = None,
                     min_rows: int = 1) -> bool:
        """
        Validate loaded data meets requirements.
        
        Args:
            data: DataFrame to validate
            required_columns: List of required column names
            min_rows: Minimum number of rows required
            
        Returns:
            True if data is valid, False otherwise
        """
        try:
            # Check minimum rows
            if len(data) < min_rows:
                logger.error(f"Data has {len(data)} rows, minimum required: {min_rows}")
                return False
            
            # Check required columns
            if required_columns:
                missing_columns = set(required_columns) - set(data.columns)
                if missing_columns:
                    logger.error(f"Missing required columns: {missing_columns}")
                    return False
            
            # Check for completely empty DataFrame
            if data.empty:
                logger.error("Data is empty")
                return False
            
            logger.info("Data validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Error during data validation: {str(e)}")
            return False
