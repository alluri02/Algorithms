"""
Main data pipeline orchestrator for AI-powered customer segmentation.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional
import logging
import time
import joblib

# Import pipeline components
from ..data_ingestion.data_generator import CustomerDataGenerator
from ..data_ingestion.data_loader import DataLoader
from ..preprocessing.data_cleaner import DataCleaner
from ..segmentation.clustering_model import ClusteringModel
from ..visualization.segment_visualizer import SegmentVisualizer

logger = logging.getLogger(__name__)


class DataPipeline:
    """Main pipeline orchestrator for customer segmentation."""
    
    def __init__(self, config=None):
        """
        Initialize the data pipeline.
        
        Args:
            config: Pipeline configuration object
        """
        self.config = config
        self.data_generator = CustomerDataGenerator()
        self.data_loader = DataLoader()
        self.data_cleaner = DataCleaner()
        self.clustering_model = ClusteringModel()
        self.visualizer = SegmentVisualizer()
        
        # Pipeline state
        self.raw_data = None
        self.processed_data = None
        self.cluster_labels = None
        self.results = {}
        
        # Create output directories
        self.setup_directories()
    
    def setup_directories(self):
        """Create necessary directories for pipeline outputs."""
        directories = [
            "data/raw",
            "data/processed", 
            "data/output",
            "models",
            "visualizations",
            "reports"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def run(self) -> Dict[str, Any]:
        """
        Run the complete data segmentation pipeline.
        
        Returns:
            Dictionary with pipeline results
        """
        logger.info("Starting AI-powered data segmentation pipeline")
        start_time = time.time()
        
        try:
            # Step 1: Data Generation/Loading
            self.raw_data = self.generate_or_load_data()
            
            # Step 2: Data Preprocessing
            self.processed_data = self.preprocess_data(self.raw_data)
            
            # Step 3: Feature Engineering
            self.processed_data = self.engineer_features(self.processed_data)
            
            # Step 4: AI Segmentation
            self.cluster_labels = self.perform_segmentation(self.processed_data)
            
            # Step 5: Post-processing and Analysis
            self.results = self.analyze_segments(
                self.processed_data, 
                self.cluster_labels
            )
            
            # Step 6: Save Results
            self.save_results()
            
            # Calculate total execution time
            execution_time = time.time() - start_time
            self.results['execution_time'] = execution_time
            
            logger.info(f"Pipeline completed successfully in {execution_time:.2f} seconds")
            
            return self.results
            
        except Exception as e:
            logger.error(f"Pipeline execution failed: {str(e)}")
            raise
    
    def generate_or_load_data(self) -> pd.DataFrame:
        """Generate synthetic data or load from existing source."""
        logger.info("Step 1: Data Generation/Loading")
        
        # Check if we should load existing data
        raw_data_path = Path("data/raw/customer_data.csv")
        
        if raw_data_path.exists() and not self.config.get('regenerate_data', False):
            logger.info("Loading existing data")
            data = self.data_loader.load_csv(raw_data_path)
        else:
            logger.info("Generating synthetic customer data")
            data = self.data_generator.generate_customer_data(
                n_customers=self.config.get('DATA_GENERATION.n_customers', 10000),
                include_noise=self.config.get('DATA_GENERATION.include_noise', True),
                noise_level=self.config.get('DATA_GENERATION.noise_level', 0.1)
            )
            
            # Save generated data
            self.data_loader.save_data(data, raw_data_path, 'csv')
        
        logger.info(f"Loaded data with shape: {data.shape}")
        return data
    
    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Preprocess and clean the data."""
        logger.info("Step 2: Data Preprocessing")
        
        # Get preprocessing configuration
        preprocessing_config = self.config.get('DATA_PROCESSING', {})
        
        # Clean the data
        processed_data = self.data_cleaner.clean_data(data, preprocessing_config)
        
        # Save processed data
        processed_path = Path("data/processed/processed_data.csv")
        self.data_loader.save_data(processed_data, processed_path, 'csv')
        
        # Generate data quality report
        quality_report = self.data_cleaner.get_data_quality_report(processed_data)
        self.results['data_quality_report'] = quality_report
        
        return processed_data
    
    def engineer_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Perform feature engineering."""
        logger.info("Step 3: Feature Engineering")
        
        # Feature engineering configuration
        fe_config = self.config.get('FEATURE_ENGINEERING', {})
        
        # Select features for clustering (exclude non-numeric and ID columns)
        exclude_columns = ['customer_id']
        feature_columns = [col for col in data.columns 
                          if col not in exclude_columns and 
                          pd.api.types.is_numeric_dtype(data[col])]
        
        # Create feature matrix
        feature_data = data[feature_columns].copy()
        
        # Add interaction features if configured
        if fe_config.get('create_interaction_features', False):
            feature_data = self.create_interaction_features(feature_data)
        
        # Feature selection if configured
        if fe_config.get('feature_selection', False):
            feature_data = self.select_features(
                feature_data, 
                method=fe_config.get('selection_method', 'variance'),
                n_features=fe_config.get('n_features', 20)
            )
        
        logger.info(f"Feature engineering completed. Final features: {feature_data.shape[1]}")
        
        return feature_data
    
    def create_interaction_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create interaction features between important variables."""
        logger.info("Creating interaction features")
        
        # Define key feature pairs for interactions
        interaction_pairs = [
            ('total_spend', 'customer_lifetime'),
            ('purchase_frequency', 'avg_order_value'),
            ('website_visits', 'email_open_rate'),
            ('age', 'income'),
            ('customer_value_score', 'engagement_score')
        ]
        
        feature_data = data.copy()
        
        for feature1, feature2 in interaction_pairs:
            if feature1 in data.columns and feature2 in data.columns:
                interaction_name = f"{feature1}_x_{feature2}"
                feature_data[interaction_name] = data[feature1] * data[feature2]
                
                # Also create ratio features
                ratio_name = f"{feature1}_div_{feature2}"
                feature_data[ratio_name] = data[feature1] / (data[feature2] + 1e-6)
        
        return feature_data
    
    def select_features(self, 
                       data: pd.DataFrame,
                       method: str = 'variance',
                       n_features: int = 20) -> pd.DataFrame:
        """Select most important features."""
        from sklearn.feature_selection import VarianceThreshold, SelectKBest, f_classif
        from sklearn.ensemble import RandomForestClassifier
        
        logger.info(f"Selecting top {n_features} features using {method} method")
        
        if method == 'variance':
            # Remove low variance features
            selector = VarianceThreshold(threshold=0.01)
            selected_data = selector.fit_transform(data)
            selected_features = data.columns[selector.get_support()]
            
            # If still too many features, select top variance ones
            if len(selected_features) > n_features:
                variances = data[selected_features].var()
                top_features = variances.nlargest(n_features).index
                return data[top_features]
            
            return data[selected_features]
        
        elif method == 'correlation':
            # Remove highly correlated features
            corr_matrix = data.corr().abs()
            upper_triangle = corr_matrix.where(
                np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
            )
            
            # Find highly correlated features
            to_drop = [column for column in upper_triangle.columns 
                      if any(upper_triangle[column] > 0.95)]
            
            selected_data = data.drop(columns=to_drop)
            
            # Select top variance features if still too many
            if len(selected_data.columns) > n_features:
                variances = selected_data.var()
                top_features = variances.nlargest(n_features).index
                return selected_data[top_features]
            
            return selected_data
        
        else:
            # Default: select by variance
            variances = data.var()
            top_features = variances.nlargest(n_features).index
            return data[top_features]
    
    def perform_segmentation(self, data: pd.DataFrame) -> np.ndarray:
        """Perform AI-powered customer segmentation."""
        logger.info("Step 4: AI Segmentation")
        
        segmentation_config = self.config.get('SEGMENTATION', {})
        method = segmentation_config.get('method', 'kmeans')
        
        if method == 'kmeans':
            # Find optimal number of clusters if not specified
            n_clusters = segmentation_config.get('n_segments', None)
            if n_clusters is None:
                optimal_k, metrics = self.clustering_model.find_optimal_clusters(
                    data, method='kmeans'
                )
                n_clusters = optimal_k
                self.results['optimization_metrics'] = metrics
            
            # Fit K-means model
            kmeans_config = segmentation_config.get('kmeans', {}).copy()
            # Remove n_clusters from config to avoid duplicate parameter
            kmeans_config.pop('n_clusters', None)
            
            labels = self.clustering_model.fit_kmeans(
                data,
                n_clusters=n_clusters,
                **kmeans_config
            )
            
        elif method == 'dbscan':
            # Use configured parameters or find optimal ones
            eps = segmentation_config.get('dbscan', {}).get('eps')
            min_samples = segmentation_config.get('dbscan', {}).get('min_samples')
            
            if eps is None or min_samples is None:
                optimal_params, metrics = self.clustering_model.find_optimal_clusters(
                    data, method='dbscan'
                )
                if eps is None:
                    eps = metrics['optimal_eps']
                if min_samples is None:
                    min_samples = optimal_params
                self.results['optimization_metrics'] = metrics
            
            # Fit DBSCAN model
            labels = self.clustering_model.fit_dbscan(
                data,
                eps=eps,
                min_samples=min_samples,
                **{k: v for k, v in segmentation_config.get('dbscan', {}).items() 
                   if k not in ['eps', 'min_samples']}
            )
        
        else:
            raise ValueError(f"Unknown segmentation method: {method}")
        
        # Save the fitted model
        model_path = Path("models/segmentation_model.joblib")
        joblib.dump(self.clustering_model, model_path)
        
        return labels
    
    def analyze_segments(self, 
                        data: pd.DataFrame,
                        labels: np.ndarray) -> Dict[str, Any]:
        """Analyze and characterize the discovered segments."""
        logger.info("Step 5: Segment Analysis")
        
        results = {
            'n_records': len(data),
            'n_segments': len(set(labels)) - (1 if -1 in labels else 0),
            'method': self.config.get('SEGMENTATION.method', 'unknown'),
            'cluster_labels': labels,
            'clustering_metrics': self.clustering_model.metrics
        }
        
        # Get cluster summary
        cluster_summary = self.clustering_model.get_cluster_summary(
            data.values, 
            feature_names=list(data.columns)
        )
        results['cluster_summary'] = cluster_summary
        
        # Add original customer data for segment profiling
        if self.raw_data is not None:
            # Map clusters back to original customers
            segment_profiles = self.create_segment_profiles(labels)
            results['segment_profiles'] = segment_profiles
        
        return results
    
    def create_segment_profiles(self, labels: np.ndarray) -> Dict[str, Any]:
        """Create business-meaningful profiles for each segment."""
        profiles = {}
        
        # Add cluster labels to processed data (which matches the labels)
        data_with_segments = self.processed_data.copy()
        data_with_segments['segment'] = labels
        
        for segment_id in sorted(set(labels)):
            if segment_id == -1:  # Skip noise points
                continue
            
            segment_data = data_with_segments[data_with_segments['segment'] == segment_id]
            
            # Calculate segment characteristics using available columns
            profile = {
                'size': len(segment_data),
                'percentage': len(segment_data) / len(data_with_segments) * 100,
                'statistics': {}
            }
            
            # Add statistics for key columns if they exist
            key_columns = ['age', 'income', 'total_spend', 'purchase_frequency', 
                          'avg_order_value', 'customer_lifetime', 'website_visits',
                          'email_open_rate', 'app_usage', 'satisfaction_score',
                          'customer_value_score', 'engagement_score']
            
            for col in key_columns:
                if col in segment_data.columns:
                    profile['statistics'][f'avg_{col}'] = segment_data[col].mean()
                    profile['statistics'][f'std_{col}'] = segment_data[col].std()
            
            # Generate segment description
            profile['description'] = self.generate_segment_description(profile)
            
            profiles[f'segment_{segment_id}'] = profile
        
        return profiles
    
    def generate_segment_description(self, profile: Dict[str, Any]) -> str:
        """Generate a human-readable description for a segment."""
        size_pct = profile['percentage']
        size = profile['size']
        stats = profile['statistics']
        
        # Build description based on available statistics
        description_parts = [
            f"This segment represents {size_pct:.1f}% of customers ({size:,} customers)"
        ]
        
        # Add key characteristics if available
        if 'avg_total_spend' in stats:
            avg_spend = stats['avg_total_spend']
            if avg_spend > 0.5:  # Normalized values
                spend_level = "high-spend"
            elif avg_spend > 0:
                spend_level = "medium-spend" 
            else:
                spend_level = "low-spend"
            description_parts.append(f"and are {spend_level} customers")
        
        if 'avg_customer_value_score' in stats:
            value_score = stats['avg_customer_value_score']
            if value_score > 0.5:
                value_level = "high-value"
            elif value_score > 0:
                value_level = "medium-value"
            else:
                value_level = "low-value"
            description_parts.append(f"with {value_level} profiles")
        
        if 'avg_satisfaction_score' in stats:
            satisfaction = stats['avg_satisfaction_score']
            if satisfaction > 0.5:
                satisfaction_level = "highly satisfied"
            elif satisfaction > 0:
                satisfaction_level = "moderately satisfied"
            else:
                satisfaction_level = "less satisfied"
            description_parts.append(f"who are {satisfaction_level}")
        
        return ". ".join(description_parts) + "."
    
    def save_results(self):
        """Save pipeline results to various formats."""
        logger.info("Step 6: Saving Results")
        
        output_config = self.config.get('OUTPUT', {})
        
        if output_config.get('save_results', True):
            # Save segmented data using processed data (which matches the cluster labels)
            if self.processed_data is not None and self.cluster_labels is not None:
                segmented_data = self.processed_data.copy()
                segmented_data['segment'] = self.cluster_labels
                
                # Save in multiple formats
                for format_type in output_config.get('output_format', ['csv']):
                    output_path = Path(f"data/output/segmented_customers.{format_type}")
                    self.data_loader.save_data(segmented_data, output_path, format_type)
            
            # Save results summary
            import json
            results_path = Path("data/output/segmentation_results.json")
            
            # Convert numpy arrays to lists for JSON serialization
            serializable_results = self.make_json_serializable(self.results.copy())
            
            with open(results_path, 'w') as f:
                json.dump(serializable_results, f, indent=2)
        
        logger.info("Results saved successfully")
    
    def make_json_serializable(self, obj):
        """Convert numpy arrays and other non-serializable objects to JSON-compatible format."""
        if isinstance(obj, dict):
            return {key: self.make_json_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self.make_json_serializable(item) for item in obj]
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.float64, np.float32)):
            return float(obj)
        else:
            return obj
    
    def generate_visualizations(self):
        """Generate visualizations for the segmentation results."""
        logger.info("Generating visualizations")
        
        if self.processed_data is not None and self.cluster_labels is not None:
            # Reduce dimensions for visualization
            data_2d = self.clustering_model.reduce_dimensions_for_visualization(
                self.processed_data
            )
            
            # Generate various plots
            self.visualizer.create_cluster_scatter_plot(
                data_2d, 
                self.cluster_labels,
                save_path="visualizations/cluster_scatter.png"
            )
            
            self.visualizer.create_segment_profile_plots(
                self.processed_data,
                self.cluster_labels,
                save_dir="visualizations"
            )
            
            logger.info("Visualizations generated successfully")
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """Get current status of the pipeline."""
        return {
            'raw_data_loaded': self.raw_data is not None,
            'data_processed': self.processed_data is not None,
            'segmentation_completed': self.cluster_labels is not None,
            'results_available': bool(self.results),
            'data_shape': self.raw_data.shape if self.raw_data is not None else None,
            'n_features': self.processed_data.shape[1] if self.processed_data is not None else None,
            'n_segments': len(set(self.cluster_labels)) - (1 if -1 in self.cluster_labels else 0) if self.cluster_labels is not None else None
        }
