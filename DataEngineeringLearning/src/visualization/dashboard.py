"""
Interactive dashboard for customer segmentation results.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


def create_dashboard(results: Dict[str, Any]):
    """
    Create interactive Streamlit dashboard.
    
    Args:
        results: Pipeline results dictionary
    """
    st.set_page_config(
        page_title="Customer Segmentation Dashboard",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("🎯 AI-Powered Customer Segmentation Dashboard")
    st.markdown("---")
    
    # Sidebar with summary metrics
    st.sidebar.header("📈 Summary Metrics")
    st.sidebar.metric("Total Customers", f"{results.get('n_records', 'N/A'):,}")
    st.sidebar.metric("Number of Segments", results.get('n_segments', 'N/A'))
    st.sidebar.metric("Segmentation Method", results.get('method', 'N/A').title())
    
    if 'execution_time' in results:
        st.sidebar.metric("Execution Time", f"{results['execution_time']:.2f}s")
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "👥 Segment Profiles", "📈 Analytics", "🔍 Data Quality"])
    
    with tab1:
        display_overview(results)
    
    with tab2:
        display_segment_profiles(results)
    
    with tab3:
        display_analytics(results)
    
    with tab4:
        display_data_quality(results)


def display_overview(results: Dict[str, Any]):
    """Display overview section of the dashboard."""
    st.header("📊 Segmentation Overview")
    
    # Segment distribution
    if 'segment_profiles' in results:
        profiles = results['segment_profiles']
        
        # Create segment size chart
        segments = []
        sizes = []
        percentages = []
        
        for segment_id, profile in profiles.items():
            segments.append(segment_id.replace('segment_', 'Segment '))
            sizes.append(profile['size'])
            percentages.append(profile['percentage'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart
            fig_pie = px.pie(
                values=sizes,
                names=segments,
                title="Customer Distribution Across Segments",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Bar chart
            fig_bar = px.bar(
                x=segments,
                y=sizes,
                title="Segment Sizes",
                color=segments,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_bar.update_layout(showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # Clustering metrics
    if 'clustering_metrics' in results:
        st.subheader("🎯 Clustering Performance Metrics")
        metrics = results['clustering_metrics']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'silhouette_score' in metrics:
                st.metric("Silhouette Score", f"{metrics['silhouette_score']:.3f}")
        
        with col2:
            if 'calinski_harabasz_score' in metrics:
                st.metric("Calinski-Harabasz Score", f"{metrics['calinski_harabasz_score']:.2f}")
        
        with col3:
            if 'inertia' in metrics:
                st.metric("Inertia", f"{metrics['inertia']:.2f}")


def display_segment_profiles(results: Dict[str, Any]):
    """Display segment profiles section."""
    st.header("👥 Detailed Segment Profiles")
    
    if 'segment_profiles' not in results:
        st.warning("Segment profiles not available.")
        return
    
    profiles = results['segment_profiles']
    
    # Segment selector
    segment_names = list(profiles.keys())
    selected_segment = st.selectbox(
        "Select a segment to explore:",
        segment_names,
        format_func=lambda x: x.replace('segment_', 'Segment ')
    )
    
    if selected_segment:
        profile = profiles[selected_segment]
        
        # Display segment description
        st.subheader(f"📋 {selected_segment.replace('segment_', 'Segment ')} Profile")
        st.info(profile.get('description', 'No description available.'))
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Size", f"{profile['size']:,}")
        with col2:
            st.metric("Percentage", f"{profile['percentage']:.1f}%")
        with col3:
            st.metric("Avg Age", f"{profile['demographics']['avg_age']:.0f}")
        with col4:
            st.metric("Avg Income", f"${profile['demographics']['avg_income']:,.0f}")
        
        # Detailed characteristics
        st.subheader("📊 Detailed Characteristics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**💰 Financial Profile**")
            st.write(f"• Average Total Spend: ${profile['behavior']['avg_total_spend']:,.0f}")
            st.write(f"• Average Order Value: ${profile['behavior']['avg_order_value']:.0f}")
            st.write(f"• Purchase Frequency: {profile['behavior']['avg_purchase_frequency']:.1f}/month")
            st.write(f"• Customer Lifetime: {profile['behavior']['avg_customer_lifetime']:.0f} months")
        
        with col2:
            st.markdown("**🎯 Engagement Profile**")
            st.write(f"• Website Visits: {profile['engagement']['avg_website_visits']:.1f}/month")
            st.write(f"• Email Open Rate: {profile['engagement']['avg_email_open_rate']:.1%}")
            st.write(f"• App Usage Rate: {profile['engagement']['app_usage_rate']:.1%}")
            st.write(f"• Satisfaction Score: {profile['satisfaction']['avg_satisfaction_score']:.1f}/10")


def display_analytics(results: Dict[str, Any]):
    """Display analytics section."""
    st.header("📈 Advanced Analytics")
    
    if 'segment_profiles' not in results:
        st.warning("Analytics data not available.")
        return
    
    profiles = results['segment_profiles']
    
    # Prepare data for comparison charts
    segments = []
    spend_data = []
    engagement_data = []
    satisfaction_data = []
    
    for segment_id, profile in profiles.items():
        segments.append(segment_id.replace('segment_', 'Segment '))
        spend_data.append(profile['behavior']['avg_total_spend'])
        engagement_data.append(profile['engagement']['avg_website_visits'])
        satisfaction_data.append(profile['satisfaction']['avg_satisfaction_score'])
    
    # Create comparison charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Spending comparison
        fig_spend = px.bar(
            x=segments,
            y=spend_data,
            title="Average Total Spend by Segment",
            color=segments,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_spend.update_layout(showlegend=False)
        st.plotly_chart(fig_spend, use_container_width=True)
    
    with col2:
        # Satisfaction comparison
        fig_satisfaction = px.bar(
            x=segments,
            y=satisfaction_data,
            title="Average Satisfaction Score by Segment",
            color=segments,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_satisfaction.update_layout(showlegend=False)
        st.plotly_chart(fig_satisfaction, use_container_width=True)
    
    # Radar chart for segment comparison
    st.subheader("🕸️ Multi-dimensional Segment Comparison")
    
    # Prepare radar chart data
    categories = ['Total Spend', 'Purchase Frequency', 'Website Visits', 'Satisfaction', 'Engagement']
    
    fig = go.Figure()
    
    colors = px.colors.qualitative.Set3[:len(segments)]
    
    for i, (segment_id, profile) in enumerate(profiles.items()):
        values = [
            profile['behavior']['avg_total_spend'] / max(spend_data),
            profile['behavior']['avg_purchase_frequency'] / max([p['behavior']['avg_purchase_frequency'] for p in profiles.values()]),
            profile['engagement']['avg_website_visits'] / max([p['engagement']['avg_website_visits'] for p in profiles.values()]),
            profile['satisfaction']['avg_satisfaction_score'] / 10,
            profile['engagement']['avg_email_open_rate']
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=segment_id.replace('segment_', 'Segment '),
            line_color=colors[i]
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title="Normalized Segment Comparison"
    )
    
    st.plotly_chart(fig, use_container_width=True)


def display_data_quality(results: Dict[str, Any]):
    """Display data quality section."""
    st.header("🔍 Data Quality Report")
    
    if 'data_quality_report' not in results:
        st.warning("Data quality report not available.")
        return
    
    quality_report = results['data_quality_report']
    
    # Basic data info
    st.subheader("📋 Dataset Information")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", f"{quality_report['shape'][0]:,}")
    with col2:
        st.metric("Total Features", quality_report['shape'][1])
    with col3:
        st.metric("Duplicate Rows", quality_report['duplicate_rows'])
    with col4:
        st.metric("Memory Usage", f"{quality_report['memory_usage_mb']:.1f} MB")
    
    # Missing values analysis
    st.subheader("❓ Missing Values Analysis")
    missing_data = quality_report.get('missing_values', {})
    
    if missing_data:
        # Filter out columns with no missing values
        missing_filtered = {k: v for k, v in missing_data.items() if v > 0}
        
        if missing_filtered:
            fig_missing = px.bar(
                x=list(missing_filtered.keys()),
                y=list(missing_filtered.values()),
                title="Missing Values by Column",
                color_discrete_sequence=['#ff6b6b']
            )
            st.plotly_chart(fig_missing, use_container_width=True)
        else:
            st.success("✅ No missing values detected!")
    
    # Data types
    st.subheader("🏷️ Data Types")
    if 'data_types' in quality_report:
        dtypes_df = pd.DataFrame(
            list(quality_report['data_types'].items()),
            columns=['Column', 'Data Type']
        )
        st.dataframe(dtypes_df, use_container_width=True)
    
    # Outliers information
    if 'potential_outliers' in quality_report:
        st.subheader("⚠️ Potential Outliers")
        outliers = quality_report['potential_outliers']
        outliers_filtered = {k: v for k, v in outliers.items() if v > 0}
        
        if outliers_filtered:
            fig_outliers = px.bar(
                x=list(outliers_filtered.keys()),
                y=list(outliers_filtered.values()),
                title="Potential Outliers by Column",
                color_discrete_sequence=['#ffa726']
            )
            st.plotly_chart(fig_outliers, use_container_width=True)
        else:
            st.success("✅ No significant outliers detected!")


def run_dashboard():
    """Main function to run the Streamlit dashboard."""
    try:
        # Load results from file
        import json
        from pathlib import Path
        
        results_path = Path("data/output/segmentation_results.json")
        
        if results_path.exists():
            with open(results_path, 'r') as f:
                results = json.load(f)
            
            create_dashboard(results)
        else:
            st.error("❌ No segmentation results found. Please run the pipeline first.")
            st.info("Run `python main.py` to generate segmentation results.")
    
    except Exception as e:
        st.error(f"❌ Error loading dashboard: {str(e)}")
        logger.error(f"Dashboard error: {str(e)}")


if __name__ == "__main__":
    run_dashboard()
