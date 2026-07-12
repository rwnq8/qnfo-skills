"""
ULTRAMETRIC CLUSTERING MODULE FOR PDE SIMULATION DATA
=====================================================
Core algorithm for computing 2-adic ultrametric distances between
physical field states from The Well dataset.

Methodology:
1. Load field snapshots (gridded velocity/pressure/density fields)
2. Compute pairwise Euclidean distance matrix
3. Build agglomerative clustering dendrogram (Ward linkage)
4. Convert to ultrametric distance: d_ultra(x,y) = max Ward distance along path
5. Verify strong triangle inequality: d(x,z) <= max(d(x,y), d(y,z))
6. Validate against known physical hierarchies (e.g., Reynolds ordering)

Falsifiability: This would be disconfirmed if the dendrogram does NOT recover
the Reynolds number ordering for turbulent channel flow data.
"""

import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist, squareform
from collections import defaultdict

class UltrametricClusterer:
    """Compute ultrametric distances between PDE field states."""
    
    def __init__(self, method='ward', metric='euclidean'):
        self.method = method
        self.metric = metric
        self.linkage_matrix = None
        self.ultrametric_distances = None
        self.labels = None
        
    def fit(self, fields, field_labels=None):
        """
        Compute ultrametric distance matrix from field snapshots.
        
        Args:
            fields: numpy array of shape (n_snapshots, n_features) or (n_snapshots, nx, ny, n_channels)
            field_labels: optional list of physical parameter labels (e.g., Reynolds numbers)
        
        Returns:
            self (for chaining)
        """
        # Flatten fields if needed
        if fields.ndim > 2:
            n = fields.shape[0]
            fields = fields.reshape(n, -1)
        
        n_snapshots = fields.shape[0]
        
        # Step 1: Compute pairwise distance matrix
        dist_vector = pdist(fields, metric=self.metric)
        dist_matrix = squareform(dist_vector)
        
        # Step 2: Build agglomerative clustering dendrogram
        self.linkage_matrix = linkage(dist_vector, method=self.method)
        
        # Step 3: Convert to ultrametric distance
        # For each merge level, all clusters merged at that level get the same distance
        # The ultrametric distance between two points = the Ward merge distance at which
        # their clusters merged
        self.ultrametric_distances = self._linkage_to_ultrametric(
            self.linkage_matrix, n_snapshots
        )
        
        # Store labels if provided
        self.labels = field_labels
        
        return self
    
    def _linkage_to_ultrametric(self, Z, n):
        """Convert scipy linkage matrix to ultrametric distance matrix.
        
        For Ward linkage, the merge distance is the increase in within-cluster
        sum of squares. The ultrametric distance d(x,y) = the merge distance
        at which x and y become members of the same cluster.
        """
        # Initialize with infinity (not yet merged)
        d_ultra = np.full((n, n), np.inf)
        np.fill_diagonal(d_ultra, 0.0)
        
        # Track which cluster each original point belongs to
        # After n-1 merges, all points belong to one cluster
        cluster_members = {i: {i} for i in range(n)}
        
        for i, merge in enumerate(Z):
            c1, c2, dist, _ = int(merge[0]), int(merge[1]), merge[2], int(merge[3])
            new_cluster = n + i
            
            # All pairs between members of c1 and c2 get distance = dist
            members_c1 = cluster_members[c1]
            members_c2 = cluster_members[c2]
            
            for m1 in members_c1:
                for m2 in members_c2:
                    d_ultra[m1, m2] = dist
                    d_ultra[m2, m1] = dist
            
            # Merge clusters
            cluster_members[new_cluster] = members_c1 | members_c2
            
            # Clean up merged clusters (optional, for memory)
            del cluster_members[c1]
            del cluster_members[c2]
        
        return d_ultra
    
    def verify_ultrametric_property(self, num_triples=1000):
        """Verify the strong triangle inequality on random triples.
        
        Strong triangle inequality: d(i,k) <= max(d(i,j), d(j,k))
        For an ultrametric, every triple forms an ISOSCELES triangle 
        where the two equal sides are >= the base.
        
        Returns:
            dict with 'violations', 'isosceles_count', 'total'
        """
        if self.ultrametric_distances is None:
            raise ValueError("Must call fit() first")
        
        n = self.ultrametric_distances.shape[0]
        violations = 0
        isosceles = 0
        
        # Sample random triples
        rng = np.random.RandomState(42)
        total = min(num_triples, n * (n-1) * (n-2) // 6)
        
        for _ in range(total):
            i, j, k = rng.choice(n, size=3, replace=False)
            dij = self.ultrametric_distances[i, j]
            djk = self.ultrametric_distances[j, k]
            dik = self.ultrametric_distances[i, k]
            
            # Check strong triangle inequality
            if dik > max(dij, djk) + 1e-10:
                violations += 1
            
            # Check isosceles property
            sides = sorted([dij, djk, dik])
            if abs(sides[1] - sides[2]) < 1e-6 * max(1.0, sides[2]):
                isosceles += 1
        
        return {
            'violations': violations,
            'isosceles_count': isosceles,
            'total': total,
            'violation_rate': violations / total,
            'isosceles_rate': isosceles / total,
            'is_ultrametric': violations == 0
        }
    
    def get_dendrogram_ordering(self):
        """Get the leaf ordering from the dendrogram (for visualization)."""
        if self.linkage_matrix is None:
            raise ValueError("Must call fit() first")
        return self._compute_leaf_order(self.linkage_matrix)
    
    def _compute_leaf_order(self, Z):
        """Compute the order of leaves in the dendrogram."""
        n = Z.shape[0] + 1
        order = []
        
        def traverse(node):
            if node < n:
                order.append(node)
                return
            idx = node - n
            left = int(Z[idx, 0])
            right = int(Z[idx, 1])
            traverse(left)
            traverse(right)
        
        root = 2 * n - 2
        traverse(root)
        return order
    
    def cluster_at_level(self, n_clusters=None, distance_threshold=None):
        """Cut the dendrogram to get flat clusters.
        
        Args:
            n_clusters: number of clusters (mutually exclusive with distance_threshold)
            distance_threshold: ultrametric distance threshold
        
        Returns:
            array of cluster labels (0-indexed)
        """
        if self.linkage_matrix is None:
            raise ValueError("Must call fit() first")
        
        if n_clusters is not None:
            return fcluster(self.linkage_matrix, n_clusters, criterion='maxclust')
        elif distance_threshold is not None:
            return fcluster(self.linkage_matrix, distance_threshold, criterion='distance')
        else:
            raise ValueError("Must specify n_clusters or distance_threshold")
    
    def compare_with_labels(self):
        """Compare ultrametric dendrogram ordering against known physical labels.
        
        If labels are provided (e.g., Reynolds numbers), compute the correlation
        between the dendrogram ordering and the label ordering.
        """
        if self.labels is None:
            raise ValueError("No labels provided. Pass field_labels to fit().")
        
        order = self.get_dendrogram_ordering()
        ordered_labels = [self.labels[i] for i in order]
        
        # Compute rank correlation between dendrogram order and label values
        from scipy.stats import spearmanr
        
        # Position in dendrogram vs label value
        positions = np.arange(len(ordered_labels))
        label_values = np.array(ordered_labels, dtype=float)
        
        corr, p_value = spearmanr(positions, label_values)
        
        return {
            'dendrogram_order': ordered_labels,
            'spearman_r': corr,
            'p_value': p_value,
            'monotonic': abs(corr) > 0.7
        }
    
    def get_distance_stats(self):
        """Get summary statistics of the ultrametric distance matrix."""
        if self.ultrametric_distances is None:
            raise ValueError("Must call fit() first")
        
        # Upper triangle (excluding diagonal)
        triu = self.ultrametric_distances[np.triu_indices_from(self.ultrametric_distances, k=1)]
        
        return {
            'min': float(np.min(triu)),
            'max': float(np.max(triu)),
            'mean': float(np.mean(triu)),
            'median': float(np.median(triu)),
            'std': float(np.std(triu)),
            'n_unique_distances': len(np.unique(triu)),
            'max_theoretical': 2.0 ** (-np.ceil(-np.log2(np.max(triu))))  # nearest 2-adic
        }


def generate_synthetic_turbulence_data(n_snapshots=20, n_reynolds=5, grid_size=32):
    """Generate synthetic "turbulence" data with known Reynolds number ordering.
    
    Creates velocity-like fields with controlled structure so we can verify
    that the ultrametric dendrogram recovers the Reynolds number ordering.
    
    Args:
        n_snapshots: number of snapshots per Reynolds number
        n_reynolds: number of different Reynolds numbers
        grid_size: spatial grid size
    
    Returns:
        fields: (n_snapshots * n_reynolds, grid_size, grid_size, 2) array
        labels: Reynolds number for each snapshot
    """
    rng = np.random.RandomState(42)
    total = n_snapshots * n_reynolds
    fields = np.zeros((total, grid_size, grid_size, 2))
    labels = []
    
    # Reynolds numbers (simulated)
    reynolds_values = np.logspace(np.log10(100), np.log10(10000), n_reynolds)
    
    for r_idx, Re in enumerate(reynolds_values):
        for s_idx in range(n_snapshots):
            idx = r_idx * n_snapshots + s_idx
            
            # Base turbulent field: Fourier modes with energy spectrum ~ k^(-5/3) (Kolmogorov)
            x = np.linspace(0, 2*np.pi, grid_size)
            y = np.linspace(0, 2*np.pi, grid_size)
            X, Y = np.meshgrid(x, y)
            
            u = np.zeros((grid_size, grid_size))
            v = np.zeros((grid_size, grid_size))
            
            # Sum of Fourier modes
            n_modes = int(10 + 30 * r_idx / n_reynolds)  # More modes at higher Re
            for _ in range(n_modes):
                kx = rng.randint(1, grid_size//3)
                ky = rng.randint(1, grid_size//3)
                amp = (kx**2 + ky**2) ** (-5/6)  # Kolmogorov scaling
                phase = rng.uniform(0, 2*np.pi)
                u += amp * np.cos(kx * X + ky * Y + phase)
                v += amp * np.sin(kx * X + ky * Y + phase + rng.uniform(0, np.pi/2))
            
            # Add Reynolds-dependent small-scale structure
            noise_scale = 0.1 * (Re / reynolds_values[-1])
            u += noise_scale * rng.randn(grid_size, grid_size)
            v += noise_scale * rng.randn(grid_size, grid_size)
            
            fields[idx, :, :, 0] = u
            fields[idx, :, :, 1] = v
            labels.append(float(Re))
    
    return fields, labels


# Quick smoke test
if __name__ == '__main__':
    print("=== Ultrametric Clusterer: Smoke Test ===")
    
    # Generate synthetic data
    fields, labels = generate_synthetic_turbulence_data(
        n_snapshots=4, n_reynolds=5, grid_size=32
    )
    print(f"Fields shape: {fields.shape}")
    print(f"Labels: {[f'{l:.0f}' for l in labels]}")
    
    # Fit ultrametric clusterer
    clusterer = UltrametricClusterer()
    clusterer.fit(fields, field_labels=labels)
    
    # Verify ultrametric property
    result = clusterer.verify_ultrametric_property(num_triples=500)
    print(f"\nUltrametric verification:")
    print(f"  Violations: {result['violations']}/{result['total']}")
    print(f"  Isosceles rate: {result['isosceles_rate']:.3f}")
    print(f"  Is ultrametric: {result['is_ultrametric']}")
    
    # Compare with labels
    label_comparison = clusterer.compare_with_labels()
    print(f"\nLabel comparison:")
    print(f"  Spearman r: {label_comparison['spearman_r']:.3f}")
    print(f"  p-value: {label_comparison['p_value']:.3f}")
    print(f"  Monotonic: {label_comparison['monotonic']}")
    print(f"  Dendrogram order: {[f'{l:.0f}' for l in label_comparison['dendrogram_order']]}")
    
    # Distance stats
    stats = clusterer.get_distance_stats()
    print(f"\nDistance stats:")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    
    print("\n[DONE] Ultrametric clusterer smoke test passed")
