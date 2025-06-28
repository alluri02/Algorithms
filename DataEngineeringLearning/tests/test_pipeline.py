"""
Test suite for the AI-powered data segmentation pipeline.
"""

import unittest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import shutil

# Import modules to test
import sys
sys.path.append('../src')

from src.data_ingestion.data_generator import CustomerDataGenerator
from src.data_ingestion.data_loader import DataLoader
from src.preprocessing.data_cleaner import DataCleaner
from src.segmentation.clustering_model import ClusteringModel
from src.pipeline.pipeline_config import PipelineConfig


class TestDataGeneration(unittest.TestCase):
    """Test data generation functionality."""
    
    def setUp(self):
        self.generator = CustomerDataGenerator(random_seed=42)
    
    def test_data_generation_shape(self):
        """Test that generated data has correct shape."""
        data = self.generator.generate_customer_data(n_customers=1000)
        self.assertEqual(len(data), 1000)
        self.assertGreater(len(data.columns), 10)
    
    def test_data_generation_columns(self):
        """Test that required columns are present."""
        data = self.generator.generate_customer_data(n_customers=100)
        required_columns = ['customer_id', 'age', 'income', 'total_spend']
        for col in required_columns:
            self.assertIn(col, data.columns)
    
    def test_data_types(self):
        """Test that data types are correct."""
        data = self.generator.generate_customer_data(n_customers=100)
        self.assertTrue(pd.api.types.is_numeric_dtype(data['age']))
        self.assertTrue(pd.api.types.is_numeric_dtype(data['income']))
        self.assertTrue(pd.api.types.is_numeric_dtype(data['total_spend']))


class TestDataLoader(unittest.TestCase):
    """Test data loading functionality."""
    
    def setUp(self):
        self.loader = DataLoader()
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test data
        self.test_data = pd.DataFrame({
            'id': [1, 2, 3],
            'value': [10, 20, 30],
            'category': ['A', 'B', 'C']
        })
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_csv_save_load(self):
        """Test CSV save and load functionality."""
        csv_path = Path(self.temp_dir) / "test.csv"
        
        # Save data
        self.loader.save_data(self.test_data, csv_path, 'csv')
        self.assertTrue(csv_path.exists())
        
        # Load data
        loaded_data = self.loader.load_csv(csv_path)
        pd.testing.assert_frame_equal(self.test_data, loaded_data)
    
    def test_data_validation(self):
        """Test data validation functionality."""
        # Valid data
        self.assertTrue(self.loader.validate_data(self.test_data, min_rows=1))
        
        # Invalid data (empty)
        empty_data = pd.DataFrame()
        self.assertFalse(self.loader.validate_data(empty_data, min_rows=1))
        
        # Missing required columns
        required_cols = ['missing_column']
        self.assertFalse(self.loader.validate_data(self.test_data, required_columns=required_cols))


class TestDataCleaner(unittest.TestCase):
    """Test data cleaning functionality."""
    
    def setUp(self):
        self.cleaner = DataCleaner()
        
        # Create test data with issues
        self.dirty_data = pd.DataFrame({
            'feature1': [1, 2, 3, 100, 5],  # Contains outlier
            'feature2': [10, 20, np.nan, 40, 50],  # Contains missing value
            'feature3': [0.1, 0.2, 0.3, 0.4, 0.5]
        })
    
    def test_missing_value_handling(self):
        """Test missing value imputation."""
        cleaned = self.cleaner.handle_missing_values(self.dirty_data, strategy='median')
        self.assertFalse(cleaned.isnull().any().any())
    
    def test_outlier_removal(self):
        """Test outlier removal."""
        original_length = len(self.dirty_data)
        cleaned = self.cleaner.remove_outliers(self.dirty_data, method='iqr', threshold=1.5)
        # Should remove the outlier (value 100)
        self.assertLess(len(cleaned), original_length)
    
    def test_feature_normalization(self):
        """Test feature normalization."""
        data_no_missing = self.dirty_data.fillna(self.dirty_data.median())
        normalized = self.cleaner.normalize_features(data_no_missing, method='standard')
        
        # Check that numerical features are normalized (mean ~0, std ~1)
        for col in normalized.select_dtypes(include=[np.number]).columns:
            self.assertAlmostEqual(normalized[col].mean(), 0, places=1)
            self.assertAlmostEqual(normalized[col].std(), 1, places=1)


class TestClusteringModel(unittest.TestCase):
    """Test clustering model functionality."""
    
    def setUp(self):
        self.model = ClusteringModel()
        
        # Create simple test data
        np.random.seed(42)
        self.test_data = pd.DataFrame({
            'feature1': np.random.randn(100),
            'feature2': np.random.randn(100),
            'feature3': np.random.randn(100)
        })
    
    def test_kmeans_clustering(self):
        """Test K-means clustering."""
        labels = self.model.fit_kmeans(self.test_data, n_clusters=3, random_state=42)
        
        self.assertEqual(len(labels), len(self.test_data))
        self.assertEqual(len(set(labels)), 3)
        self.assertIsNotNone(self.model.model)
    
    def test_dbscan_clustering(self):
        """Test DBSCAN clustering."""
        labels = self.model.fit_dbscan(self.test_data, eps=0.5, min_samples=5)
        
        self.assertEqual(len(labels), len(self.test_data))
        self.assertIsNotNone(self.model.model)
    
    def test_optimal_clusters_finding(self):
        """Test optimal cluster number finding."""
        optimal_k, metrics = self.model.find_optimal_clusters(
            self.test_data, method='kmeans', max_clusters=5, min_clusters=2
        )
        
        self.assertGreaterEqual(optimal_k, 2)
        self.assertLessEqual(optimal_k, 5)
        self.assertIn('silhouette_scores', metrics)
        self.assertIn('inertias', metrics)
    
    def test_cluster_summary(self):
        """Test cluster summary generation."""
        labels = self.model.fit_kmeans(self.test_data, n_clusters=3, random_state=42)
        summary = self.model.get_cluster_summary(self.test_data.values, list(self.test_data.columns))
        
        self.assertIsInstance(summary, dict)
        self.assertEqual(len(summary), 3)  # 3 clusters


class TestPipelineConfig(unittest.TestCase):
    """Test pipeline configuration functionality."""
    
    def setUp(self):
        self.config = PipelineConfig()
    
    def test_config_loading(self):
        """Test configuration loading."""
        self.assertIsInstance(self.config.config, dict)
        self.assertIn('DATA_GENERATION', self.config.config)
        self.assertIn('SEGMENTATION', self.config.config)
    
    def test_config_get(self):
        """Test configuration value retrieval."""
        # Test direct key
        n_customers = self.config.get('DATA_GENERATION.n_customers', 1000)
        self.assertIsInstance(n_customers, int)
        
        # Test default value
        missing_value = self.config.get('NON_EXISTENT_KEY', 'default')
        self.assertEqual(missing_value, 'default')
    
    def test_config_update(self):
        """Test configuration value update."""
        original_value = self.config.get('DATA_GENERATION.n_customers')
        new_value = 5000
        
        self.config.update('DATA_GENERATION.n_customers', new_value)
        updated_value = self.config.get('DATA_GENERATION.n_customers')
        
        self.assertEqual(updated_value, new_value)
        self.assertNotEqual(updated_value, original_value)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete pipeline."""
    
    def test_mini_pipeline(self):
        """Test a mini version of the complete pipeline."""
        # Generate small dataset
        generator = CustomerDataGenerator(random_seed=42)
        data = generator.generate_customer_data(n_customers=200)
        
        # Clean data
        cleaner = DataCleaner()
        config = {
            'remove_outliers': True,
            'fill_missing': True,
            'normalize_features': True
        }
        cleaned_data = cleaner.clean_data(data, config)
        
        # Select features
        feature_cols = ['age', 'income', 'total_spend', 'customer_value_score']
        available_features = [col for col in feature_cols if col in cleaned_data.columns]
        feature_data = cleaned_data[available_features]
        
        # Perform clustering
        model = ClusteringModel()
        labels = model.fit_kmeans(feature_data, n_clusters=3, random_state=42)
        
        # Verify results
        self.assertEqual(len(labels), len(feature_data))
        self.assertGreaterEqual(len(set(labels)), 1)
        self.assertLessEqual(len(set(labels)), 3)
        self.assertIsNotNone(model.metrics.get('silhouette_score'))


if __name__ == '__main__':
    unittest.main()
