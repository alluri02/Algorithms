"""
Segment visualization and dashboard creation.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

# Set style for matplotlib
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


class SegmentVisualizer:
    """Create visualizations for customer segmentation results."""
    
    def __init__(self, output_dir: str = "visualizations"):
        """
        Initialize the visualizer.
        
        Args:
            output_dir: Directory to save visualizations
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_cluster_scatter_plot(self, 
                                   data_2d: np.ndarray,
                                   labels: np.ndarray,
                                   save_path: Optional[str] = None) -> None:
        """
        Create 2D scatter plot of clusters.
        
        Args:
            data_2d: 2D reduced data for plotting
            labels: Cluster labels
            save_path: Path to save the plot
        """
        logger.info("Creating cluster scatter plot")
        
        plt.figure(figsize=(12, 8))
        
        # Create scatter plot for each cluster
        unique_labels = sorted(set(labels))
        colors = plt.cm.Set3(np.linspace(0, 1, len(unique_labels)))
        
        for i, label in enumerate(unique_labels):
            if label == -1:  # Noise points (DBSCAN)
                plt.scatter(data_2d[labels == label, 0], 
                           data_2d[labels == label, 1],
                           c='black', marker='x', s=50, alpha=0.5, 
                           label='Noise')
            else:
                plt.scatter(data_2d[labels == label, 0], 
                           data_2d[labels == label, 1],
                           c=[colors[i]], s=60, alpha=0.7, 
                           label=f'Segment {label}')
        
        plt.xlabel('First Principal Component')
        plt.ylabel('Second Principal Component')
        plt.title('Customer Segments Visualization (PCA)')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Cluster scatter plot saved to {save_path}")
        
        plt.show()
    
    def create_segment_profile_plots(self, 
                                   data: pd.DataFrame,
                                   labels: np.ndarray,
                                   save_dir: Optional[str] = None) -> None:
        """
        Create comprehensive segment profile visualizations.
        
        Args:
            data: Original customer data
            labels: Cluster labels
            save_dir: Directory to save plots
        """
        logger.info("Creating segment profile plots")
        
        # Add segment labels to data
        data_with_segments = data.copy()
        data_with_segments['segment'] = labels
        
        # Remove noise points for cleaner visualization
        data_with_segments = data_with_segments[data_with_segments['segment'] != -1]
        
        if save_dir:
            save_dir = Path(save_dir)
            save_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Segment size distribution
        self._plot_segment_sizes(data_with_segments, save_dir)
        
        # 2. Demographics by segment
        self._plot_demographics(data_with_segments, save_dir)
        
        # 3. Spending behavior by segment
        self._plot_spending_behavior(data_with_segments, save_dir)
        
        # 4. Engagement metrics by segment
        self._plot_engagement_metrics(data_with_segments, save_dir)
        
        # 5. Feature importance heatmap
        self._plot_feature_heatmap(data_with_segments, save_dir)
        
        logger.info("Segment profile plots created successfully")
    
    def _plot_segment_sizes(self, data: pd.DataFrame, save_dir: Optional[Path]) -> None:
        """Plot segment size distribution."""
        plt.figure(figsize=(10, 6))
        
        segment_counts = data['segment'].value_counts().sort_index()
        segment_percentages = (segment_counts / len(data) * 100).round(1)
        
        bars = plt.bar(range(len(segment_counts)), segment_counts.values, 
                      color='skyblue', alpha=0.7, edgecolor='navy')
        
        # Add percentage labels on bars
        for i, (count, pct) in enumerate(zip(segment_counts.values, segment_percentages.values)):
            plt.text(i, count + max(segment_counts) * 0.01, 
                    f'{pct}%', ha='center', va='bottom', fontweight='bold')
        
        plt.xlabel('Segment')
        plt.ylabel('Number of Customers')
        plt.title('Customer Distribution Across Segments')
        plt.xticks(range(len(segment_counts)), 
                  [f'Segment {i}' for i in segment_counts.index])
        plt.grid(True, alpha=0.3, axis='y')
        
        if save_dir:
            plt.savefig(save_dir / 'segment_sizes.png', dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def _plot_demographics(self, data: pd.DataFrame, save_dir: Optional[Path]) -> None:
        """Plot demographic characteristics by segment."""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Age distribution
        sns.boxplot(data=data, x='segment', y='age', ax=axes[0, 0])
        axes[0, 0].set_title('Age Distribution by Segment')
        axes[0, 0].set_xlabel('Segment')
        
        # Income distribution
        sns.boxplot(data=data, x='segment', y='income', ax=axes[0, 1])
        axes[0, 1].set_title('Income Distribution by Segment')
        axes[0, 1].set_xlabel('Segment')
        axes[0, 1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
        
        # Region distribution (if region column exists)
        if 'region' in data.columns:
            region_segment = pd.crosstab(data['segment'], data['region'], normalize='index') * 100
            region_segment.plot(kind='bar', ax=axes[1, 0], stacked=True)
            axes[1, 0].set_title('Regional Distribution by Segment (%)')
            axes[1, 0].set_xlabel('Segment')
            axes[1, 0].set_ylabel('Percentage')
            axes[1, 0].legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left')
        else:
            # Plot alternative metric if region is not available
            if 'app_usage' in data.columns:
                sns.boxplot(data=data, x='segment', y='app_usage', ax=axes[1, 0])
                axes[1, 0].set_title('App Usage by Segment')
                axes[1, 0].set_xlabel('Segment')
                axes[1, 0].set_ylabel('App Usage Score')
            else:
                axes[1, 0].text(0.5, 0.5, 'Region data not available', 
                               transform=axes[1, 0].transAxes, ha='center', va='center')
        
        # Customer lifetime
        sns.boxplot(data=data, x='segment', y='customer_lifetime', ax=axes[1, 1])
        axes[1, 1].set_title('Customer Lifetime by Segment')
        axes[1, 1].set_xlabel('Segment')
        axes[1, 1].set_ylabel('Months')
        
        plt.tight_layout()
        
        if save_dir:
            plt.savefig(save_dir / 'demographics.png', dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def _plot_spending_behavior(self, data: pd.DataFrame, save_dir: Optional[Path]) -> None:
        """Plot spending behavior by segment."""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Total spend
        sns.boxplot(data=data, x='segment', y='total_spend', ax=axes[0, 0])
        axes[0, 0].set_title('Total Spend by Segment')
        axes[0, 0].set_xlabel('Segment')
        axes[0, 0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
        
        # Average order value
        sns.boxplot(data=data, x='segment', y='avg_order_value', ax=axes[0, 1])
        axes[0, 1].set_title('Average Order Value by Segment')
        axes[0, 1].set_xlabel('Segment')
        axes[0, 1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:.0f}'))
        
        # Purchase frequency
        sns.boxplot(data=data, x='segment', y='purchase_frequency', ax=axes[1, 0])
        axes[1, 0].set_title('Purchase Frequency by Segment')
        axes[1, 0].set_xlabel('Segment')
        axes[1, 0].set_ylabel('Purchases per Month')
        
        # Recency (if available)
        if 'recency' in data.columns:
            sns.boxplot(data=data, x='segment', y='recency', ax=axes[1, 1])
            axes[1, 1].set_title('Recency by Segment')
            axes[1, 1].set_xlabel('Segment')
            axes[1, 1].set_ylabel('Days Since Last Purchase')
        elif 'customer_lifetime' in data.columns:
            sns.boxplot(data=data, x='segment', y='customer_lifetime', ax=axes[1, 1])
            axes[1, 1].set_title('Customer Lifetime by Segment')
            axes[1, 1].set_xlabel('Segment')
            axes[1, 1].set_ylabel('Customer Lifetime Value')
        else:
            axes[1, 1].text(0.5, 0.5, 'Recency data not available', 
                           transform=axes[1, 1].transAxes, ha='center', va='center')
        
        plt.tight_layout()
        
        if save_dir:
            plt.savefig(save_dir / 'spending_behavior.png', dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def _plot_engagement_metrics(self, data: pd.DataFrame, save_dir: Optional[Path]) -> None:
        """Plot engagement metrics by segment."""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Website visits
        sns.boxplot(data=data, x='segment', y='website_visits', ax=axes[0, 0])
        axes[0, 0].set_title('Website Visits by Segment')
        axes[0, 0].set_xlabel('Segment')
        
        # Email open rate
        sns.boxplot(data=data, x='segment', y='email_open_rate', ax=axes[0, 1])
        axes[0, 1].set_title('Email Open Rate by Segment')
        axes[0, 1].set_xlabel('Segment')
        axes[0, 1].set_ylabel('Open Rate')
        
        # App usage
        app_usage = pd.crosstab(data['segment'], data['app_usage'], normalize='index') * 100
        app_usage.plot(kind='bar', ax=axes[1, 0])
        axes[1, 0].set_title('App Usage by Segment (%)')
        axes[1, 0].set_xlabel('Segment')
        axes[1, 0].set_ylabel('Percentage')
        axes[1, 0].legend(['No App Usage', 'App Usage'])
        
        # Satisfaction score (if available)
        if 'satisfaction_score' in data.columns:
            sns.boxplot(data=data, x='segment', y='satisfaction_score', ax=axes[1, 1])
            axes[1, 1].set_title('Satisfaction Score by Segment')
            axes[1, 1].set_xlabel('Segment')
            axes[1, 1].set_ylabel('Score (0-10)')
        elif 'engagement_score' in data.columns:
            sns.boxplot(data=data, x='segment', y='engagement_score', ax=axes[1, 1])
            axes[1, 1].set_title('Engagement Score by Segment')
            axes[1, 1].set_xlabel('Segment')
            axes[1, 1].set_ylabel('Engagement Score')
        else:
            axes[1, 1].text(0.5, 0.5, 'Satisfaction data not available', 
                           transform=axes[1, 1].transAxes, ha='center', va='center')
        
        plt.tight_layout()
        
        if save_dir:
            plt.savefig(save_dir / 'engagement_metrics.png', dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def _plot_feature_heatmap(self, data: pd.DataFrame, save_dir: Optional[Path]) -> None:
        """Plot feature importance heatmap across segments."""
        # Select key numerical features
        key_features = [
            'age', 'income', 'total_spend', 'avg_order_value', 'purchase_frequency',
            'website_visits', 'email_open_rate', 'satisfaction_score', 'recency',
            'customer_value_score', 'engagement_score', 'risk_score'
        ]
        
        # Filter features that exist in the data
        available_features = [f for f in key_features if f in data.columns]
        
        # Calculate mean values for each segment
        segment_profiles = data.groupby('segment')[available_features].mean()
        
        # Normalize values for better visualization
        segment_profiles_norm = segment_profiles.div(segment_profiles.max(), axis=1)
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(segment_profiles_norm.T, annot=True, cmap='RdYlBu_r', 
                   center=0.5, fmt='.2f', cbar_kws={'label': 'Normalized Value'})
        plt.title('Segment Profile Heatmap (Normalized Features)')
        plt.xlabel('Segment')
        plt.ylabel('Features')
        plt.tight_layout()
        
        if save_dir:
            plt.savefig(save_dir / 'feature_heatmap.png', dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def create_interactive_dashboard(self, 
                                   data: pd.DataFrame,
                                   labels: np.ndarray,
                                   segment_profiles: Dict[str, Any]) -> go.Figure:
        """
        Create an interactive Plotly dashboard.
        
        Args:
            data: Original customer data
            labels: Cluster labels
            segment_profiles: Segment profile information
            
        Returns:
            Plotly figure object
        """
        logger.info("Creating interactive dashboard")
        
        # Add segment labels to data
        data_with_segments = data.copy()
        data_with_segments['segment'] = labels
        
        # Remove noise points
        data_with_segments = data_with_segments[data_with_segments['segment'] != -1]
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Segment Distribution', 'Age vs Income by Segment',
                          'Total Spend Distribution', 'Engagement vs Value Score'),
            specs=[[{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "box"}, {"type": "scatter"}]]
        )
        
        # 1. Segment distribution
        segment_counts = data_with_segments['segment'].value_counts().sort_index()
        fig.add_trace(
            go.Bar(x=[f'Segment {i}' for i in segment_counts.index], 
                  y=segment_counts.values,
                  name='Segment Size'),
            row=1, col=1
        )
        
        # 2. Age vs Income scatter
        colors = px.colors.qualitative.Set3[:len(segment_counts)]
        for i, segment in enumerate(sorted(data_with_segments['segment'].unique())):
            segment_data = data_with_segments[data_with_segments['segment'] == segment]
            fig.add_trace(
                go.Scatter(x=segment_data['age'], y=segment_data['income'],
                          mode='markers', name=f'Segment {segment}',
                          marker=dict(color=colors[i], size=8, opacity=0.6)),
                row=1, col=2
            )
        
        # 3. Total spend box plot
        for i, segment in enumerate(sorted(data_with_segments['segment'].unique())):
            segment_data = data_with_segments[data_with_segments['segment'] == segment]
            fig.add_trace(
                go.Box(y=segment_data['total_spend'], name=f'Segment {segment}',
                      marker_color=colors[i]),
                row=2, col=1
            )
        
        # 4. Engagement vs Value scatter
        for i, segment in enumerate(sorted(data_with_segments['segment'].unique())):
            segment_data = data_with_segments[data_with_segments['segment'] == segment]
            fig.add_trace(
                go.Scatter(x=segment_data['engagement_score'], 
                          y=segment_data['customer_value_score'],
                          mode='markers', name=f'Segment {segment}',
                          marker=dict(color=colors[i], size=8, opacity=0.6)),
                row=2, col=2
            )
        
        # Update layout
        fig.update_layout(
            title="Customer Segmentation Dashboard",
            height=800,
            showlegend=True,
            template="plotly_white"
        )
        
        # Update axes labels
        fig.update_xaxes(title_text="Age", row=1, col=2)
        fig.update_yaxes(title_text="Income", row=1, col=2)
        fig.update_yaxes(title_text="Total Spend", row=2, col=1)
        fig.update_xaxes(title_text="Engagement Score", row=2, col=2)
        fig.update_yaxes(title_text="Customer Value Score", row=2, col=2)
        
        return fig
    
    def create_segment_comparison_radar(self, 
                                      data: pd.DataFrame,
                                      labels: np.ndarray,
                                      save_path: Optional[str] = None) -> None:
        """
        Create radar chart comparing segments across key metrics.
        
        Args:
            data: Original customer data
            labels: Cluster labels
            save_path: Path to save the plot
        """
        logger.info("Creating segment comparison radar chart")
        
        # Add segment labels to data
        data_with_segments = data.copy()
        data_with_segments['segment'] = labels
        
        # Remove noise points
        data_with_segments = data_with_segments[data_with_segments['segment'] != -1]
        
        # Define key metrics for comparison
        metrics = [
            'customer_value_score', 'engagement_score', 'satisfaction_score',
            'total_spend', 'purchase_frequency', 'avg_order_value'
        ]
        
        # Filter available metrics
        available_metrics = [m for m in metrics if m in data_with_segments.columns]
        
        # Calculate segment means and normalize
        segment_means = data_with_segments.groupby('segment')[available_metrics].mean()
        segment_means_norm = segment_means.div(segment_means.max(), axis=0)
        
        # Create radar chart using plotly
        fig = go.Figure()
        
        colors = px.colors.qualitative.Set3[:len(segment_means_norm)]
        
        for i, (segment, values) in enumerate(segment_means_norm.iterrows()):
            fig.add_trace(go.Scatterpolar(
                r=values.values.tolist() + [values.values[0]],  # Close the polygon
                theta=available_metrics + [available_metrics[0]],
                fill='toself',
                name=f'Segment {segment}',
                line_color=colors[i],
                fillcolor=colors[i],
                opacity=0.6
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title="Segment Comparison Radar Chart"
        )
        
        if save_path:
            fig.write_image(save_path)
            logger.info(f"Radar chart saved to {save_path}")
        
        fig.show()
    
    def save_all_visualizations(self, 
                              data: pd.DataFrame,
                              labels: np.ndarray,
                              data_2d: Optional[np.ndarray] = None) -> None:
        """
        Generate and save all visualization types.
        
        Args:
            data: Original customer data
            labels: Cluster labels
            data_2d: 2D reduced data for scatter plot
        """
        logger.info("Generating and saving all visualizations")
        
        # Create cluster scatter plot if 2D data is available
        if data_2d is not None:
            self.create_cluster_scatter_plot(
                data_2d, labels, 
                save_path=str(self.output_dir / "cluster_scatter.png")
            )
        
        # Create segment profile plots
        self.create_segment_profile_plots(data, labels, str(self.output_dir))
        
        # Create radar chart
        self.create_segment_comparison_radar(
            data, labels,
            save_path=str(self.output_dir / "segment_radar.png")
        )
        
        logger.info(f"All visualizations saved to {self.output_dir}")
