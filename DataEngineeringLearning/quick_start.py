#!/usr/bin/env python3
"""
Quick start script for the AI-powered customer segmentation pipeline.
This script demonstrates how to use the pipeline with minimal setup.
"""

import os
import sys
from pathlib import Path

# Add src to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

def main():
    """Run a quick demonstration of the segmentation pipeline."""
    print("🚀 AI-Powered Customer Segmentation Pipeline")
    print("=" * 50)
    
    try:
        # Import after adding to path
        from data_ingestion.data_generator import CustomerDataGenerator
        from preprocessing.data_cleaner import DataCleaner
        from segmentation.clustering_model import ClusteringModel
        from visualization.segment_visualizer import SegmentVisualizer
        
        print("✅ Successfully imported pipeline components")
        
        # Step 1: Generate sample data
        print("\n📊 Step 1: Generating sample customer data...")
        generator = CustomerDataGenerator(random_seed=42)
        data = generator.generate_customer_data(n_customers=2000, include_noise=True)
        print(f"   Generated {len(data)} customer records with {len(data.columns)} features")
        
        # Step 2: Data preprocessing
        print("\n🔧 Step 2: Preprocessing data...")
        cleaner = DataCleaner()
        config = {
            'remove_outliers': True,
            'outlier_method': 'iqr',
            'fill_missing': True,
            'missing_strategy': 'median',
            'normalize_features': True,
            'normalization_method': 'standard'
        }
        
        processed_data = cleaner.clean_data(data, config)
        print(f"   Processed data shape: {processed_data.shape}")
        
        # Step 3: Feature selection
        print("\n🎯 Step 3: Selecting features for clustering...")
        feature_columns = [
            'age', 'income', 'total_spend', 'avg_order_value', 'purchase_frequency',
            'customer_value_score', 'engagement_score', 'satisfaction_score'
        ]
        
        # Filter available features
        available_features = [col for col in feature_columns if col in processed_data.columns]
        feature_data = processed_data[available_features]
        print(f"   Selected {len(available_features)} features: {available_features}")
        
        # Step 4: AI-powered segmentation
        print("\n🤖 Step 4: Performing AI-powered segmentation...")
        clustering_model = ClusteringModel()
        
        # Find optimal clusters
        optimal_k, metrics = clustering_model.find_optimal_clusters(
            feature_data, method='kmeans', max_clusters=6, min_clusters=2
        )
        print(f"   Optimal number of clusters: {optimal_k}")
        print(f"   Best silhouette score: {metrics['silhouette_scores'][optimal_k-2]:.3f}")
        
        # Perform clustering
        labels = clustering_model.fit_kmeans(feature_data, n_clusters=optimal_k, random_state=42)
        print(f"   Clustering completed with {len(set(labels))} segments")
        
        # Step 5: Analyze results
        print("\n📈 Step 5: Analyzing segments...")
        
        # Add segments to processed data (which matches the clustering results)
        segmented_data = processed_data.copy()
        segmented_data['segment'] = labels
        
        # Display segment summary
        segment_summary = segmented_data.groupby('segment').agg({
            'age': 'mean',
            'income': 'mean', 
            'total_spend': 'mean',
            'customer_value_score': 'mean',
            'satisfaction_score': 'mean'
        }).round(2)
        
        print("\n📊 Segment Profiles:")
        print(segment_summary)
        
        # Segment sizes
        segment_counts = segmented_data['segment'].value_counts().sort_index()
        segment_percentages = (segment_counts / len(segmented_data) * 100).round(1)
        
        print(f"\n👥 Segment Distribution:")
        for segment_id in segment_counts.index:
            count = segment_counts[segment_id]
            pct = segment_percentages[segment_id]
            print(f"   Segment {segment_id}: {count:,} customers ({pct}%)")
        
        # Step 6: Generate insights
        print("\n💡 Step 6: Business insights...")
        
        insights = []
        
        # High-value segment
        high_value_segment = segment_summary['total_spend'].idxmax()
        high_value_spend = segment_summary.loc[high_value_segment, 'total_spend']
        insights.append(f"🔥 Segment {high_value_segment} is the highest-value segment with average spend of ${high_value_spend:,.0f}")
        
        # Most satisfied segment
        most_satisfied_segment = segment_summary['satisfaction_score'].idxmax()
        satisfaction_score = segment_summary.loc[most_satisfied_segment, 'satisfaction_score']
        insights.append(f"😊 Segment {most_satisfied_segment} has the highest satisfaction score ({satisfaction_score:.1f}/10)")
        
        # Largest segment
        largest_segment = segment_counts.idxmax()
        largest_size = segment_counts[largest_segment]
        insights.append(f"👥 Segment {largest_segment} is the largest segment with {largest_size:,} customers")
        
        print("\n🎯 Key Business Insights:")
        for insight in insights:
            print(f"   • {insight}")
        
        # Step 7: Create basic visualization
        print("\n📊 Step 7: Creating visualizations...")
        try:
            # Ensure visualizations directory exists
            vis_dir = project_root / "visualizations"
            vis_dir.mkdir(exist_ok=True)
            
            # Create visualizer
            visualizer = SegmentVisualizer(str(vis_dir))
            
            # Create 2D visualization
            data_2d = clustering_model.reduce_dimensions_for_visualization(feature_data)
            visualizer.create_cluster_scatter_plot(
                data_2d, labels, 
                save_path=str(vis_dir / "quick_start_segments.png")
            )
            
            print(f"   ✅ Visualization saved to {vis_dir / 'quick_start_segments.png'}")
            
        except Exception as e:
            print(f"   ⚠️ Could not create visualizations: {str(e)}")
        
        # Save results
        print("\n💾 Step 8: Saving results...")
        try:
            output_dir = project_root / "data" / "output"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Save segmented data
            segmented_data.to_csv(output_dir / "quick_start_results.csv", index=False)
            print(f"   ✅ Results saved to {output_dir / 'quick_start_results.csv'}")
            
        except Exception as e:
            print(f"   ⚠️ Could not save results: {str(e)}")
        
        print("\n🎉 Pipeline demonstration completed successfully!")
        print("\nNext steps:")
        print("• Run 'python main.py' for the full pipeline")
        print("• Open 'notebooks/customer_segmentation_analysis.ipynb' for interactive analysis")
        print("• Use 'docker-compose up' for containerized deployment")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install the required dependencies:")
        print("pip install -r requirements.txt")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
