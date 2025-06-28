# AI-Powered Data Segmentation Pipeline

This project demonstrates how to build a data pipeline that uses AI/ML for customer segmentation. The pipeline includes data ingestion, preprocessing, AI-based segmentation, and visualization components.

## Project Structure

```
├── src/
│   ├── data_ingestion/
│   │   ├── __init__.py
│   │   ├── data_generator.py      # Generate synthetic customer data
│   │   └── data_loader.py         # Load data from various sources
│   ├── preprocessing/
│   │   ├── __init__.py
│   │   ├── data_cleaner.py        # Clean and validate data
│   │   └── feature_engineer.py    # Feature engineering
│   ├── segmentation/
│   │   ├── __init__.py
│   │   ├── clustering_model.py    # K-means, DBSCAN clustering
│   │   ├── ml_segmentation.py     # ML-based segmentation
│   │   └── ai_segmentation.py     # Advanced AI segmentation
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── data_pipeline.py       # Main pipeline orchestrator
│   │   └── pipeline_config.py     # Configuration management
│   └── visualization/
│       ├── __init__.py
│       ├── segment_visualizer.py  # Visualize segments
│       └── dashboard.py           # Interactive dashboard
├── data/
│   ├── raw/                       # Raw input data
│   ├── processed/                 # Processed data
│   └── output/                    # Segmentation results
├── notebooks/                     # Jupyter notebooks for analysis
├── tests/                         # Unit tests
├── config/                        # Configuration files
├── requirements.txt               # Python dependencies
├── docker-compose.yml             # Docker setup
└── main.py                        # Entry point
```

## Features

- **Data Generation**: Synthetic customer data generation
- **Data Preprocessing**: Cleaning, validation, and feature engineering
- **AI Segmentation**: Multiple segmentation approaches:
  - K-means clustering
  - DBSCAN clustering
  - Random Forest-based segmentation
  - Neural Network-based segmentation
- **Pipeline Orchestration**: Configurable data pipeline
- **Visualization**: Interactive dashboards and plots
- **Containerization**: Docker support for easy deployment

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd DataEngineeringLearning
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Quick start demonstration**
   ```bash
   python quick_start.py
   ```

5. **Run the full pipeline**
   ```bash
   python main.py
   ```

### Docker Setup (Alternative)

If you prefer using Docker:

```bash
# Build and run all services
docker-compose up --build

# Run only the pipeline
docker-compose up segmentation-pipeline

# Access Jupyter notebook
# Navigate to http://localhost:8888

# Access Streamlit dashboard  
# Navigate to http://localhost:8501
```

## Usage

### 1. Quick Start Demo
```bash
python quick_start.py
```
This runs a simplified version of the pipeline with 2,000 synthetic customers and demonstrates all major features.

### 2. Full Pipeline
```bash
python main.py
```
Runs the complete pipeline with configurable parameters.

### 3. Interactive Analysis
```bash
jupyter lab notebooks/customer_segmentation_analysis.ipynb
```
Open the Jupyter notebook for step-by-step interactive analysis.

### 4. Web Dashboard
```bash
streamlit run src/visualization/dashboard.py
```
Launch an interactive web dashboard to explore results.

### 5. Custom Configuration
Modify `config/pipeline_config.yaml` to customize:
- Data generation parameters
- Preprocessing options
- Segmentation algorithms
- Visualization settings

### Example Configurations

**K-means with 4 segments:**
```yaml
SEGMENTATION:
  method: "kmeans"
  n_segments: 4
  kmeans:
    n_clusters: 4
    random_state: 42
```

**DBSCAN clustering:**
```yaml
SEGMENTATION:
  method: "dbscan"
  dbscan:
    eps: 0.5
    min_samples: 5
```

## Segmentation Methods

1. **K-means Clustering**: Traditional unsupervised clustering
2. **DBSCAN**: Density-based clustering for complex shapes
3. **Random Forest**: Supervised segmentation based on features
4. **Neural Network**: Deep learning-based segmentation

## Data Features

The pipeline works with customer data including:
- Demographics (age, income, location)
- Purchase behavior (frequency, amount, categories)
- Engagement metrics (website visits, email opens)
- Temporal patterns (seasonality, trends)

## Output

The pipeline generates:
- Segment assignments for each customer
- Segment profiles and characteristics
- Visualization dashboards
- Performance metrics
- Exportable reports

## Examples and Results

### Sample Output
After running the pipeline, you'll get:

```
🚀 AI-Powered Customer Segmentation Pipeline
==================================================
✅ Successfully imported pipeline components

📊 Step 1: Generating sample customer data...
   Generated 2,000 customer records with 23 features

🔧 Step 2: Preprocessing data...
   Processed data shape: (1,847, 23)

🎯 Step 3: Selecting features for clustering...
   Selected 8 features: ['age', 'income', 'total_spend', ...]

🤖 Step 4: Performing AI-powered segmentation...
   Optimal number of clusters: 4
   Best silhouette score: 0.542

📈 Step 5: Analyzing segments...
   Clustering completed with 4 segments

👥 Segment Distribution:
   Segment 0: 425 customers (23.0%)
   Segment 1: 398 customers (21.6%) 
   Segment 2: 456 customers (24.7%)
   Segment 3: 568 customers (30.7%)
```

### Generated Files
- `data/output/segmented_customers.csv` - Customer data with segment assignments
- `data/output/segmentation_results.json` - Detailed results and metrics
- `visualizations/cluster_scatter.png` - 2D visualization of segments
- `visualizations/segment_profiles.png` - Detailed segment analysis plots

### Business Insights Example
The pipeline automatically generates business insights such as:
- 🔥 Segment 2 is the highest-value segment with average spend of $45,230
- 😊 Segment 1 has the highest satisfaction score (8.2/10)
- 👥 Segment 3 is the largest segment with 568 customers

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Make sure you're in the project directory
   cd DataEngineeringLearning
   
   # Install requirements
   pip install -r requirements.txt
   ```

2. **Memory Issues with Large Datasets**
   ```yaml
   # Reduce data size in config/pipeline_config.yaml
   DATA_GENERATION:
     n_customers: 5000  # Instead of 10000
   ```

3. **Visualization Issues**
   ```bash
   # Install additional plotting backends
   pip install matplotlib seaborn plotly kaleido
   ```

4. **Missing Dependencies**
   ```bash
   # Install specific packages
   pip install scikit-learn pandas numpy matplotlib
   ```

### Performance Tips

1. **For faster execution:**
   - Reduce `n_customers` in configuration
   - Use `parallel_processing: false` for debugging
   - Set `create_plots: false` to skip visualizations

2. **For better clustering:**
   - Increase `n_customers` for more data
   - Try different `segmentation_method` options
   - Adjust preprocessing parameters

3. **For custom data:**
   - Replace `data_generator.py` with your data source
   - Modify feature selection in `data_pipeline.py`
   - Update visualization components as needed

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and add tests
4. Run tests: `python -m pytest tests/`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues:
1. Check the troubleshooting section above
2. Review existing GitHub issues
3. Create a new issue with detailed information
4. Include error messages and system information

## Acknowledgments

- Built with scikit-learn for machine learning
- Visualizations powered by matplotlib, seaborn, and plotly  
- Interactive dashboards using Streamlit
- Container support via Docker
