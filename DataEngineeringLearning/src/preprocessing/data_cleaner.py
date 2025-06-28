"""
Data cleaning and preprocessing for the segmentation pipeline.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.impute import SimpleImputer, KNNImputer
import logging

logger = logging.getLogger(__name__)


class DataCleaner:
    """Clean and preprocess data for segmentation analysis."""
    
    def __init__(self):
        """Initialize the data cleaner."""
        self.scalers = {}
        self.imputers = {}
        self.outlier_bounds = {}
    
    def clean_data(self, 
                   data: pd.DataFrame,
                   config: Dict[str, Any]) -> pd.DataFrame:
        """
        Apply comprehensive data cleaning pipeline.
        
        Args:
            data: Input DataFrame
            config: Configuration dictionary
            
        Returns:
            Cleaned DataFrame
        """
        logger.info("Starting data cleaning pipeline")
        original_shape = data.shape
        
        # Make a copy to avoid modifying original data
        cleaned_data = data.copy()
        
        # Remove duplicates
        cleaned_data = self.remove_duplicates(cleaned_data)
        
        # Handle missing values
        if config.get('fill_missing', True):
            cleaned_data = self.handle_missing_values(
                cleaned_data, 
                strategy=config.get('missing_strategy', 'median')
            )
        
        # Remove outliers
        if config.get('remove_outliers', True):
            cleaned_data = self.remove_outliers(
                cleaned_data,
                method=config.get('outlier_method', 'iqr'),
                threshold=config.get('outlier_threshold', 1.5)
            )
        
        # Normalize features
        if config.get('normalize_features', True):
            cleaned_data = self.normalize_features(
                cleaned_data,
                method=config.get('normalization_method', 'standard')
            )
        
        # Data type optimization
        cleaned_data = self.optimize_data_types(cleaned_data)
        
        final_shape = cleaned_data.shape
        logger.info(f"Data cleaning completed. Shape: {original_shape} -> {final_shape}")
        
        # Log cleaning summary
        rows_removed = original_shape[0] - final_shape[0]
        if rows_removed > 0:
            removal_pct = (rows_removed / original_shape[0]) * 100
            logger.info(f"Removed {rows_removed} rows ({removal_pct:.2f}%)")
        
        return cleaned_data
    
    def remove_duplicates(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Remove duplicate rows from the dataset.
        
        Args:
            data: Input DataFrame
            
        Returns:
            DataFrame with duplicates removed
        """
        initial_count = len(data)
        data_cleaned = data.drop_duplicates()
        duplicates_removed = initial_count - len(data_cleaned)
        
        if duplicates_removed > 0:
            logger.info(f"Removed {duplicates_removed} duplicate rows")
        
        return data_cleaned
    
    def handle_missing_values(self, 
                            data: pd.DataFrame,
                            strategy: str = 'median') -> pd.DataFrame:
        """
        Handle missing values using various imputation strategies.
        
        Args:
            data: Input DataFrame
            strategy: Imputation strategy ('mean', 'median', 'mode', 'knn')
            
        Returns:
            DataFrame with imputed values
        """
        logger.info(f"Handling missing values using {strategy} strategy")
        
        # Identify columns with missing values
        missing_cols = data.columns[data.isnull().any()].tolist()
        
        if not missing_cols:
            logger.info("No missing values found")
            return data
        
        logger.info(f"Found missing values in {len(missing_cols)} columns: {missing_cols}")
        
        data_imputed = data.copy()
        
        if strategy == 'knn':
            # Use KNN imputer for numerical columns
            numerical_cols = data.select_dtypes(include=[np.number]).columns
            missing_numerical = [col for col in missing_cols if col in numerical_cols]
            
            if missing_numerical:
                imputer = KNNImputer(n_neighbors=5)
                data_imputed[missing_numerical] = imputer.fit_transform(
                    data_imputed[missing_numerical]
                )
                self.imputers['knn_numerical'] = imputer
            
            # Handle categorical columns separately
            categorical_cols = data.select_dtypes(include=['object', 'category']).columns
            missing_categorical = [col for col in missing_cols if col in categorical_cols]
            
            for col in missing_categorical:
                mode_value = data_imputed[col].mode().iloc[0] if len(data_imputed[col].mode()) > 0 else 'Unknown'
                data_imputed[col].fillna(mode_value, inplace=True)
        
        else:
            # Use SimpleImputer for other strategies
            numerical_cols = data.select_dtypes(include=[np.number]).columns
            categorical_cols = data.select_dtypes(include=['object', 'category']).columns
            
            # Handle numerical columns
            missing_numerical = [col for col in missing_cols if col in numerical_cols]
            if missing_numerical:
                if strategy in ['mean', 'median']:
                    imputer = SimpleImputer(strategy=strategy)
                    data_imputed[missing_numerical] = imputer.fit_transform(
                        data_imputed[missing_numerical]
                    )
                    self.imputers[f'{strategy}_numerical'] = imputer
            
            # Handle categorical columns
            missing_categorical = [col for col in missing_cols if col in categorical_cols]
            if missing_categorical:
                imputer = SimpleImputer(strategy='most_frequent')
                data_imputed[missing_categorical] = imputer.fit_transform(
                    data_imputed[missing_categorical]
                )
                self.imputers['mode_categorical'] = imputer
        
        # Log imputation results
        remaining_missing = data_imputed.isnull().sum().sum()
        logger.info(f"Missing values after imputation: {remaining_missing}")
        
        return data_imputed
    
    def remove_outliers(self, 
                       data: pd.DataFrame,
                       method: str = 'iqr',
                       threshold: float = 1.5) -> pd.DataFrame:
        """
        Remove outliers from numerical columns.
        
        Args:
            data: Input DataFrame
            method: Outlier detection method ('iqr', 'zscore')
            threshold: Threshold for outlier detection
            
        Returns:
            DataFrame with outliers removed
        """
        logger.info(f"Removing outliers using {method} method with threshold {threshold}")
        
        numerical_cols = data.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) == 0:
            logger.info("No numerical columns found for outlier removal")
            return data
        
        data_cleaned = data.copy()
        outlier_mask = pd.Series([True] * len(data_cleaned))
        
        for col in numerical_cols:
            if method == 'iqr':
                Q1 = data_cleaned[col].quantile(0.25)
                Q3 = data_cleaned[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                
                col_mask = (data_cleaned[col] >= lower_bound) & (data_cleaned[col] <= upper_bound)
                self.outlier_bounds[col] = (lower_bound, upper_bound)
                
            elif method == 'zscore':
                z_scores = np.abs((data_cleaned[col] - data_cleaned[col].mean()) / data_cleaned[col].std())
                col_mask = z_scores <= threshold
                
            else:
                logger.warning(f"Unknown outlier method: {method}. Skipping outlier removal.")
                continue
            
            outlier_mask &= col_mask
        
        data_cleaned = data_cleaned[outlier_mask]
        outliers_removed = len(data) - len(data_cleaned)
        
        if outliers_removed > 0:
            removal_pct = (outliers_removed / len(data)) * 100
            logger.info(f"Removed {outliers_removed} outlier rows ({removal_pct:.2f}%)")
        
        return data_cleaned
    
    def normalize_features(self, 
                          data: pd.DataFrame,
                          method: str = 'standard') -> pd.DataFrame:
        """
        Normalize numerical features.
        
        Args:
            data: Input DataFrame
            method: Normalization method ('standard', 'minmax', 'robust')
            
        Returns:
            DataFrame with normalized features
        """
        logger.info(f"Normalizing features using {method} method")
        
        numerical_cols = data.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) == 0:
            logger.info("No numerical columns found for normalization")
            return data
        
        data_normalized = data.copy()
        
        # Choose scaler based on method
        if method == 'standard':
            scaler = StandardScaler()
        elif method == 'minmax':
            scaler = MinMaxScaler()
        elif method == 'robust':
            scaler = RobustScaler()
        else:
            logger.warning(f"Unknown normalization method: {method}. Using standard scaling.")
            scaler = StandardScaler()
        
        # Fit and transform numerical columns
        data_normalized[numerical_cols] = scaler.fit_transform(data_normalized[numerical_cols])
        self.scalers[method] = scaler
        
        logger.info(f"Normalized {len(numerical_cols)} numerical features")
        
        return data_normalized
    
    def optimize_data_types(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Optimize data types to reduce memory usage.
        
        Args:
            data: Input DataFrame
            
        Returns:
            DataFrame with optimized data types
        """
        logger.info("Optimizing data types")
        
        data_optimized = data.copy()
        initial_memory = data_optimized.memory_usage(deep=True).sum()
        
        # Optimize numerical columns
        for col in data_optimized.select_dtypes(include=[np.number]).columns:
            col_data = data_optimized[col]
            
            # Check if column can be converted to a smaller integer type
            if col_data.dtype in ['int64', 'int32']:
                if col_data.min() >= -128 and col_data.max() <= 127:
                    data_optimized[col] = col_data.astype('int8')
                elif col_data.min() >= -32768 and col_data.max() <= 32767:
                    data_optimized[col] = col_data.astype('int16')
                elif col_data.min() >= -2147483648 and col_data.max() <= 2147483647:
                    data_optimized[col] = col_data.astype('int32')
            
            # Check if float can be converted to float32
            elif col_data.dtype == 'float64':
                if col_data.min() >= np.finfo(np.float32).min and col_data.max() <= np.finfo(np.float32).max:
                    data_optimized[col] = col_data.astype('float32')
        
        # Convert object columns to category if beneficial
        for col in data_optimized.select_dtypes(include=['object']).columns:
            unique_ratio = data_optimized[col].nunique() / len(data_optimized)
            if unique_ratio < 0.5:  # If less than 50% unique values
                data_optimized[col] = data_optimized[col].astype('category')
        
        final_memory = data_optimized.memory_usage(deep=True).sum()
        memory_reduction = (initial_memory - final_memory) / initial_memory * 100
        
        logger.info(f"Memory usage reduced by {memory_reduction:.2f}%")
        
        return data_optimized
    
    def get_data_quality_report(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate a comprehensive data quality report.
        
        Args:
            data: Input DataFrame
            
        Returns:
            Dictionary with data quality metrics
        """
        report = {
            'shape': data.shape,
            'memory_usage_mb': data.memory_usage(deep=True).sum() / 1024**2,
            'duplicate_rows': data.duplicated().sum(),
            'missing_values': data.isnull().sum().to_dict(),
            'data_types': data.dtypes.to_dict(),
        }
        
        # Numerical columns analysis
        numerical_cols = data.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) > 0:
            report['numerical_summary'] = data[numerical_cols].describe().to_dict()
            
            # Detect potential outliers
            outliers = {}
            for col in numerical_cols:
                Q1 = data[col].quantile(0.25)
                Q3 = data[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outlier_count = ((data[col] < lower_bound) | (data[col] > upper_bound)).sum()
                outliers[col] = outlier_count
            
            report['potential_outliers'] = outliers
        
        # Categorical columns analysis
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) > 0:
            categorical_info = {}
            for col in categorical_cols:
                categorical_info[col] = {
                    'unique_values': data[col].nunique(),
                    'most_frequent': data[col].mode().iloc[0] if len(data[col].mode()) > 0 else None,
                    'frequency': data[col].value_counts().iloc[0] if len(data[col]) > 0 else 0
                }
            report['categorical_summary'] = categorical_info
        
        return report
