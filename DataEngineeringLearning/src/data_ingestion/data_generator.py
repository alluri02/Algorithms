"""
Synthetic customer data generator for the segmentation pipeline.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class CustomerDataGenerator:
    """Generate synthetic customer data for segmentation analysis."""
    
    def __init__(self, random_seed: int = 42):
        """
        Initialize the data generator.
        
        Args:
            random_seed: Random seed for reproducibility
        """
        self.random_seed = random_seed
        np.random.seed(random_seed)
    
    def generate_customer_data(self, 
                             n_customers: int = 10000,
                             include_noise: bool = True,
                             noise_level: float = 0.1) -> pd.DataFrame:
        """
        Generate synthetic customer data.
        
        Args:
            n_customers: Number of customers to generate
            include_noise: Whether to add noise to the data
            noise_level: Level of noise to add (0.0 to 1.0)
            
        Returns:
            DataFrame with customer data
        """
        logger.info(f"Generating {n_customers} synthetic customer records")
        
        # Customer demographics
        customer_ids = [f"CUST_{i:06d}" for i in range(n_customers)]
        ages = np.random.normal(40, 15, n_customers)
        ages = np.clip(ages, 18, 80).astype(int)
        
        # Income distribution (log-normal)
        incomes = np.random.lognormal(10.5, 0.5, n_customers)
        incomes = np.clip(incomes, 20000, 200000).astype(int)
        
        # Geographic regions
        regions = np.random.choice(['North', 'South', 'East', 'West'], 
                                 n_customers, p=[0.3, 0.25, 0.25, 0.2])
        
        # Purchase behavior patterns
        purchase_frequency = np.random.poisson(5, n_customers)  # purchases per month
        avg_order_value = np.random.gamma(50, 2, n_customers)  # average order value
        
        # Customer lifetime (months)
        customer_lifetime = np.random.exponential(24, n_customers)
        customer_lifetime = np.clip(customer_lifetime, 1, 60).astype(int)
        
        # Total spend (based on frequency, AOV, and lifetime)
        total_spend = (purchase_frequency * avg_order_value * 
                      customer_lifetime / 12)
        
        # Digital engagement
        website_visits = np.random.poisson(10, n_customers)  # visits per month
        email_open_rate = np.random.beta(2, 5, n_customers)  # 0 to 1
        app_usage = np.random.choice([0, 1], n_customers, p=[0.4, 0.6])  # binary
        
        # Product preferences (categories)
        electronics_spend_pct = np.random.beta(2, 8, n_customers)
        clothing_spend_pct = np.random.beta(3, 7, n_customers)
        home_spend_pct = np.random.beta(2, 8, n_customers)
        
        # Normalize category percentages
        total_category_pct = (electronics_spend_pct + clothing_spend_pct + 
                            home_spend_pct)
        electronics_spend_pct /= total_category_pct
        clothing_spend_pct /= total_category_pct
        home_spend_pct /= total_category_pct
        
        # Seasonal behavior
        summer_boost = np.random.normal(1.0, 0.2, n_customers)
        holiday_boost = np.random.normal(1.5, 0.3, n_customers)
        
        # Recency (days since last purchase)
        recency = np.random.exponential(30, n_customers).astype(int)
        recency = np.clip(recency, 0, 365)
        
        # Customer satisfaction scores
        satisfaction_score = np.random.beta(4, 2, n_customers) * 10
        
        # Support interactions
        support_tickets = np.random.poisson(2, n_customers)
        
        # Create DataFrame
        data = pd.DataFrame({
            'customer_id': customer_ids,
            'age': ages,
            'income': incomes,
            'region': regions,
            'purchase_frequency': purchase_frequency,
            'avg_order_value': avg_order_value,
            'customer_lifetime': customer_lifetime,
            'total_spend': total_spend,
            'website_visits': website_visits,
            'email_open_rate': email_open_rate,
            'app_usage': app_usage,
            'electronics_spend_pct': electronics_spend_pct,
            'clothing_spend_pct': clothing_spend_pct,
            'home_spend_pct': home_spend_pct,
            'summer_boost': summer_boost,
            'holiday_boost': holiday_boost,
            'recency': recency,
            'satisfaction_score': satisfaction_score,
            'support_tickets': support_tickets
        })
        
        # Add noise if requested
        if include_noise:
            data = self._add_noise(data, noise_level)
        
        # Add some missing values to simulate real-world data
        data = self._add_missing_values(data)
        
        # Add derived features
        data = self._add_derived_features(data)
        
        logger.info(f"Generated dataset with shape: {data.shape}")
        logger.info(f"Features: {list(data.columns)}")
        
        return data
    
    def _add_noise(self, data: pd.DataFrame, noise_level: float) -> pd.DataFrame:
        """Add noise to numerical columns."""
        numerical_cols = data.select_dtypes(include=[np.number]).columns
        
        for col in numerical_cols:
            if col != 'customer_id':  # Don't add noise to ID
                noise = np.random.normal(0, noise_level * data[col].std(), 
                                       len(data))
                data[col] += noise
        
        return data
    
    def _add_missing_values(self, data: pd.DataFrame) -> pd.DataFrame:
        """Add missing values to simulate real-world data."""
        # Add missing values to some columns (5% missing)
        missing_cols = ['satisfaction_score', 'app_usage', 'email_open_rate']
        
        for col in missing_cols:
            if col in data.columns:
                missing_mask = np.random.choice([True, False], 
                                              len(data), p=[0.05, 0.95])
                data.loc[missing_mask, col] = np.nan
        
        return data
    
    def _add_derived_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Add derived features based on existing data."""
        # Customer value score
        data['customer_value_score'] = (
            (data['total_spend'] / data['total_spend'].max()) * 0.4 +
            (data['purchase_frequency'] / data['purchase_frequency'].max()) * 0.3 +
            (data['satisfaction_score'] / 10) * 0.3
        )
        
        # Engagement score
        data['engagement_score'] = (
            (data['website_visits'] / data['website_visits'].max()) * 0.4 +
            data['email_open_rate'].fillna(0) * 0.3 +
            data['app_usage'].fillna(0) * 0.3
        )
        
        # Risk score (high support tickets, low satisfaction)
        data['risk_score'] = (
            (data['support_tickets'] / data['support_tickets'].max()) * 0.6 +
            (1 - data['satisfaction_score'].fillna(5) / 10) * 0.4
        )
        
        # Seasonality index
        data['seasonality_index'] = (
            data['summer_boost'] * 0.4 + data['holiday_boost'] * 0.6
        )
        
        return data
    
    def generate_sample_segments(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate ground truth segments for evaluation purposes.
        
        Args:
            data: Customer data DataFrame
            
        Returns:
            Dictionary with segment information
        """
        # Define segments based on business logic
        segments = {}
        
        # High Value Customers
        high_value_mask = (
            (data['customer_value_score'] > 0.7) & 
            (data['total_spend'] > data['total_spend'].quantile(0.8))
        )
        segments['High Value'] = data[high_value_mask].index.tolist()
        
        # New Customers
        new_customer_mask = (
            (data['customer_lifetime'] <= 6) & 
            (data['recency'] <= 30)
        )
        segments['New Customers'] = data[new_customer_mask].index.tolist()
        
        # At Risk Customers
        at_risk_mask = (
            (data['risk_score'] > 0.6) | 
            (data['recency'] > 90)
        )
        segments['At Risk'] = data[at_risk_mask].index.tolist()
        
        # Loyal Customers
        loyal_mask = (
            (data['customer_lifetime'] > 24) & 
            (data['satisfaction_score'] > 7) &
            (data['purchase_frequency'] > data['purchase_frequency'].median())
        )
        segments['Loyal'] = data[loyal_mask].index.tolist()
        
        # Budget Conscious
        budget_mask = (
            (data['avg_order_value'] < data['avg_order_value'].quantile(0.3)) &
            (data['income'] < data['income'].median())
        )
        segments['Budget Conscious'] = data[budget_mask].index.tolist()
        
        return segments
