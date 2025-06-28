#!/usr/bin/env python3
"""
Custom pipeline runner with DBSCAN configuration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.pipeline.data_pipeline import DataPipeline
from src.pipeline.pipeline_config import PipelineConfig

def main():
    print("🔬 Running Custom DBSCAN Segmentation Pipeline")
    print("=" * 50)
    
    try:
        # Load custom configuration
        config_path = "config/dbscan_config.yaml"
        config = PipelineConfig(config_path)
        
        # Initialize and run pipeline
        pipeline = DataPipeline(config.config)
        results = pipeline.run()
        
        print("\n✅ DBSCAN Pipeline Results:")
        print(f"   Records processed: {results['n_records']}")
        print(f"   Segments created: {results['n_segments']}")
        print(f"   Method used: {results['method']}")
        
        # Generate visualizations
        print("\n📊 Generating visualizations...")
        pipeline.generate_visualizations()
        
        print("\n🎉 Custom DBSCAN pipeline completed successfully!")
        
    except Exception as e:
        print(f"❌ Pipeline failed: {str(e)}")

if __name__ == "__main__":
    main()
