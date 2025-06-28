"""
Configuration management for the data segmentation pipeline.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class PipelineConfig:
    """Configuration manager for the data segmentation pipeline."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file. If None, uses default config.
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "pipeline_config.yaml"
        
        self.config_path = Path(config_path)
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as file:
                config = yaml.safe_load(file)
            logger.info(f"Configuration loaded from {self.config_path}")
            return config
        except FileNotFoundError:
            logger.warning(f"Configuration file not found: {self.config_path}")
            return self.get_default_config()
        except yaml.YAMLError as e:
            logger.error(f"Error parsing configuration file: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration if file is not available."""
        return {
            "DATA_GENERATION": {
                "n_customers": 10000,
                "random_seed": 42,
                "include_noise": True,
                "noise_level": 0.1
            },
            "DATA_PROCESSING": {
                "remove_outliers": True,
                "outlier_method": "iqr",
                "outlier_threshold": 1.5,
                "fill_missing": True,
                "missing_strategy": "median",
                "normalize_features": True,
                "normalization_method": "standard"
            },
            "FEATURE_ENGINEERING": {
                "create_interaction_features": True,
                "polynomial_features": False,
                "polynomial_degree": 2,
                "feature_selection": True,
                "selection_method": "variance",
                "n_features": 20
            },
            "SEGMENTATION": {
                "method": "kmeans",
                "n_segments": 5,
                "kmeans": {
                    "n_clusters": 5,
                    "random_state": 42,
                    "n_init": 10,
                    "max_iter": 300
                }
            },
            "VISUALIZATION": {
                "create_plots": True,
                "plot_types": ["scatter", "heatmap", "distribution", "segment_profile"],
                "save_plots": True,
                "plot_format": "png",
                "plot_dpi": 300
            },
            "OUTPUT": {
                "save_results": True,
                "output_format": ["csv", "parquet", "json"],
                "include_metadata": True,
                "create_report": True
            },
            "PIPELINE": {
                "parallel_processing": True,
                "n_jobs": -1,
                "cache_intermediate_results": True,
                "validate_data": True,
                "log_level": "INFO",
                "start_dashboard": False
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'DATA_GENERATION.n_customers')
            default: Default value if key is not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def update(self, key: str, value: Any) -> None:
        """
        Update configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            value: New value
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        logger.info(f"Configuration updated: {key} = {value}")
    
    def save_config(self, path: Optional[str] = None) -> None:
        """
        Save current configuration to file.
        
        Args:
            path: Path to save configuration. If None, uses original config path.
        """
        save_path = Path(path) if path else self.config_path
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(save_path, 'w') as file:
            yaml.dump(self.config, file, default_flow_style=False, indent=2)
        
        logger.info(f"Configuration saved to {save_path}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary."""
        return self.config.copy()
    
    def __getitem__(self, key: str) -> Any:
        """Allow dictionary-like access."""
        return self.get(key)
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Allow dictionary-like assignment."""
        self.update(key, value)
