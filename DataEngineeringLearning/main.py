"""
Main entry point for the AI-powered data segmentation pipeline.
"""

import logging
import sys
from pathlib import Path
from typing import Dict, Any

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.pipeline.data_pipeline import DataPipeline
from src.pipeline.pipeline_config import PipelineConfig
from src.visualization.dashboard import create_dashboard

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Main function to run the data segmentation pipeline."""
    logger.info("Starting AI-powered data segmentation pipeline")
    
    try:
        # Load configuration
        config = PipelineConfig()
        
        # Initialize pipeline
        pipeline = DataPipeline(config)
        
        # Run the complete pipeline
        logger.info("Running data pipeline...")
        results = pipeline.run()
        
        # Log results summary
        logger.info(f"Pipeline completed successfully!")
        logger.info(f"Number of records processed: {results.get('n_records', 'N/A')}")
        logger.info(f"Number of segments created: {results.get('n_segments', 'N/A')}")
        logger.info(f"Segmentation method used: {results.get('method', 'N/A')}")
        
        # Generate visualizations
        logger.info("Generating visualizations...")
        pipeline.generate_visualizations()
        
        # Optionally start interactive dashboard
        if config.get('start_dashboard', False):
            logger.info("Starting interactive dashboard...")
            create_dashboard(results)
        
        logger.info("Pipeline execution completed successfully!")
        
    except Exception as e:
        logger.error(f"Pipeline execution failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()
