"""
K-means and DBSCAN clustering models for customer segmentation.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, Optional
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.decomposition import PCA
import logging

logger = logging.getLogger(__name__)


class ClusteringModel:
    """Traditional clustering algorithms for customer segmentation."""
    
    def __init__(self):
        """Initialize clustering model."""
        self.model = None
        self.model_type = None
        self.labels = None
        self.metrics = {}
        self.pca = None
    
    def fit_kmeans(self, 
                   data: pd.DataFrame,
                   n_clusters: int = 5,
                   random_state: int = 42,
                   **kwargs) -> np.ndarray:
        """
        Fit K-means clustering model.
        
        Args:
            data: Input features for clustering
            n_clusters: Number of clusters
            random_state: Random seed
            **kwargs: Additional parameters for KMeans
            
        Returns:
            Cluster labels
        """
        logger.info(f"Fitting K-means model with {n_clusters} clusters")
        
        # Initialize and fit model
        self.model = KMeans(
            n_clusters=n_clusters,
            random_state=random_state,
            n_init=kwargs.get('n_init', 10),
            max_iter=kwargs.get('max_iter', 300)
        )
        
        self.labels = self.model.fit_predict(data)
        self.model_type = 'kmeans'
        
        # Calculate metrics
        self._calculate_metrics(data, self.labels)
        
        logger.info(f"K-means clustering completed. Found {len(np.unique(self.labels))} clusters")
        
        return self.labels
    
    def fit_dbscan(self, 
                   data: pd.DataFrame,
                   eps: float = 0.5,
                   min_samples: int = 5,
                   **kwargs) -> np.ndarray:
        """
        Fit DBSCAN clustering model.
        
        Args:
            data: Input features for clustering
            eps: Maximum distance between samples in same neighborhood
            min_samples: Minimum samples in neighborhood for core point
            **kwargs: Additional parameters for DBSCAN
            
        Returns:
            Cluster labels
        """
        logger.info(f"Fitting DBSCAN model with eps={eps}, min_samples={min_samples}")
        
        # Initialize and fit model
        self.model = DBSCAN(
            eps=eps,
            min_samples=min_samples,
            metric=kwargs.get('metric', 'euclidean'),
            n_jobs=kwargs.get('n_jobs', -1)
        )
        
        self.labels = self.model.fit_predict(data)
        self.model_type = 'dbscan'
        
        # Calculate metrics (excluding noise points for DBSCAN)
        non_noise_mask = self.labels != -1
        if non_noise_mask.sum() > 0:
            self._calculate_metrics(data[non_noise_mask], self.labels[non_noise_mask])
        
        n_clusters = len(set(self.labels)) - (1 if -1 in self.labels else 0)
        n_noise = list(self.labels).count(-1)
        
        logger.info(f"DBSCAN clustering completed. Found {n_clusters} clusters and {n_noise} noise points")
        
        return self.labels
    
    def find_optimal_clusters(self, 
                            data: pd.DataFrame,
                            method: str = 'kmeans',
                            max_clusters: int = 10,
                            min_clusters: int = 2) -> Tuple[int, Dict[str, Any]]:
        """
        Find optimal number of clusters using various metrics.
        
        Args:
            data: Input features
            method: Clustering method ('kmeans' or 'dbscan')
            max_clusters: Maximum number of clusters to test
            min_clusters: Minimum number of clusters to test
            
        Returns:
            Tuple of (optimal_clusters, metrics_dict)
        """
        logger.info(f"Finding optimal number of clusters for {method}")
        
        if method == 'kmeans':
            return self._find_optimal_kmeans(data, max_clusters, min_clusters)
        elif method == 'dbscan':
            return self._find_optimal_dbscan(data)
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def _find_optimal_kmeans(self, 
                           data: pd.DataFrame,
                           max_clusters: int,
                           min_clusters: int) -> Tuple[int, Dict[str, Any]]:
        """Find optimal K for K-means using elbow method and silhouette score."""
        inertias = []
        silhouette_scores = []
        calinski_scores = []
        cluster_range = range(min_clusters, max_clusters + 1)
        
        for k in cluster_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(data)
            
            inertias.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(data, labels))
            calinski_scores.append(calinski_harabasz_score(data, labels))
        
        # Find elbow point
        optimal_k_elbow = self._find_elbow_point(list(cluster_range), inertias)
        
        # Find best silhouette score
        optimal_k_silhouette = cluster_range[np.argmax(silhouette_scores)]
        
        # Find best Calinski-Harabasz score
        optimal_k_calinski = cluster_range[np.argmax(calinski_scores)]
        
        # Combine results (prioritize silhouette score)
        optimal_k = optimal_k_silhouette
        
        metrics = {
            'cluster_range': list(cluster_range),
            'inertias': inertias,
            'silhouette_scores': silhouette_scores,
            'calinski_scores': calinski_scores,
            'optimal_k_elbow': optimal_k_elbow,
            'optimal_k_silhouette': optimal_k_silhouette,
            'optimal_k_calinski': optimal_k_calinski,
            'recommended_k': optimal_k
        }
        
        logger.info(f"Optimal K-means clusters: {optimal_k} (based on silhouette score)")
        
        return optimal_k, metrics
    
    def _find_optimal_dbscan(self, data: pd.DataFrame) -> Tuple[int, Dict[str, Any]]:
        """Find optimal parameters for DBSCAN using k-distance method."""
        from sklearn.neighbors import NearestNeighbors
        
        # Calculate k-distance for different k values
        k_values = [3, 4, 5, 6]
        eps_candidates = []
        
        for k in k_values:
            neighbors = NearestNeighbors(n_neighbors=k)
            neighbors_fit = neighbors.fit(data)
            distances, indices = neighbors_fit.kneighbors(data)
            
            # Sort distances and find elbow point
            k_distances = np.sort(distances[:, k-1], axis=0)[::-1]
            eps_candidate = self._find_elbow_point(range(len(k_distances)), k_distances)
            eps_candidates.append(k_distances[eps_candidate] if eps_candidate < len(k_distances) else k_distances[-1])
        
        # Use median eps
        optimal_eps = np.median(eps_candidates)
        
        # Test different min_samples values
        min_samples_range = [3, 4, 5, 6, 7]
        best_score = -1
        optimal_min_samples = 5
        
        for min_samples in min_samples_range:
            dbscan = DBSCAN(eps=optimal_eps, min_samples=min_samples)
            labels = dbscan.fit_predict(data)
            
            # Skip if all points are noise or only one cluster
            n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            if n_clusters > 1:
                non_noise_mask = labels != -1
                if non_noise_mask.sum() > min_samples:
                    score = silhouette_score(data[non_noise_mask], labels[non_noise_mask])
                    if score > best_score:
                        best_score = score
                        optimal_min_samples = min_samples
        
        metrics = {
            'optimal_eps': optimal_eps,
            'optimal_min_samples': optimal_min_samples,
            'eps_candidates': eps_candidates,
            'best_silhouette_score': best_score
        }
        
        logger.info(f"Optimal DBSCAN parameters: eps={optimal_eps:.3f}, min_samples={optimal_min_samples}")
        
        return optimal_min_samples, metrics
    
    def _find_elbow_point(self, x_values: list, y_values: list) -> int:
        """Find elbow point in a curve using the maximum curvature method."""
        if len(x_values) < 3:
            return 0
        
        # Calculate second derivatives (curvature)
        curvatures = []
        for i in range(1, len(y_values) - 1):
            curvature = abs(y_values[i-1] - 2*y_values[i] + y_values[i+1])
            curvatures.append(curvature)
        
        # Find maximum curvature
        if curvatures:
            elbow_idx = np.argmax(curvatures) + 1  # +1 because we started from index 1
            return elbow_idx
        
        return len(x_values) // 2  # Return middle point as fallback
    
    def _calculate_metrics(self, data: pd.DataFrame, labels: np.ndarray) -> None:
        """Calculate clustering evaluation metrics."""
        try:
            if len(set(labels)) > 1:  # Need at least 2 clusters
                self.metrics['silhouette_score'] = silhouette_score(data, labels)
                self.metrics['calinski_harabasz_score'] = calinski_harabasz_score(data, labels)
            
            # Inertia for K-means
            if self.model_type == 'kmeans':
                self.metrics['inertia'] = self.model.inertia_
            
            # General metrics
            self.metrics['n_clusters'] = len(set(labels)) - (1 if -1 in labels else 0)
            self.metrics['n_noise'] = list(labels).count(-1) if -1 in labels else 0
            
        except Exception as e:
            logger.warning(f"Error calculating metrics: {str(e)}")
    
    def reduce_dimensions_for_visualization(self, 
                                          data: pd.DataFrame,
                                          n_components: int = 2) -> np.ndarray:
        """
        Reduce dimensions using PCA for visualization.
        
        Args:
            data: Input features
            n_components: Number of components to keep
            
        Returns:
            Reduced dimensional data
        """
        logger.info(f"Reducing dimensions to {n_components} components for visualization")
        
        self.pca = PCA(n_components=n_components, random_state=42)
        data_reduced = self.pca.fit_transform(data)
        
        explained_variance = self.pca.explained_variance_ratio_.sum()
        logger.info(f"PCA explained variance: {explained_variance:.3f}")
        
        return data_reduced
    
    def get_cluster_centers(self) -> Optional[np.ndarray]:
        """
        Get cluster centers (only available for K-means).
        
        Returns:
            Cluster centers or None if not available
        """
        if self.model_type == 'kmeans' and self.model is not None:
            return self.model.cluster_centers_
        return None
    
    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """
        Predict cluster labels for new data.
        
        Args:
            data: New data to predict
            
        Returns:
            Predicted cluster labels
        """
        if self.model is None:
            raise ValueError("Model must be fitted before prediction")
        
        if self.model_type == 'kmeans':
            return self.model.predict(data)
        else:
            # DBSCAN doesn't have a predict method, would need to use fit_predict
            # or implement a custom prediction method
            raise NotImplementedError("Prediction not implemented for DBSCAN")
    
    def get_cluster_summary(self, 
                           data: pd.DataFrame,
                           feature_names: Optional[list] = None) -> Dict[str, Any]:
        """
        Get summary statistics for each cluster.
        
        Args:
            data: Original feature data
            feature_names: Names of features
            
        Returns:
            Dictionary with cluster summaries
        """
        if self.labels is None:
            raise ValueError("Model must be fitted before getting cluster summary")
        
        if feature_names is None:
            feature_names = [f"feature_{i}" for i in range(data.shape[1])]
        
        data_df = pd.DataFrame(data, columns=feature_names)
        data_df['cluster'] = self.labels
        
        summary = {}
        
        for cluster_id in sorted(set(self.labels)):
            if cluster_id == -1:  # Skip noise points in DBSCAN
                continue
                
            cluster_data = data_df[data_df['cluster'] == cluster_id]
            
            summary[f'cluster_{cluster_id}'] = {
                'size': len(cluster_data),
                'percentage': len(cluster_data) / len(data_df) * 100,
                'mean': cluster_data[feature_names].mean().to_dict(),
                'std': cluster_data[feature_names].std().to_dict(),
                'median': cluster_data[feature_names].median().to_dict()
            }
        
        return summary
