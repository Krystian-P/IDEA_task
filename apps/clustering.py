import numpy as np
from sklearn.cluster import KMeans


def clusterData(branchData, nClusters):
    array = branchData[:, 2]
    kmeans = KMeans(copy_x=True, init='k-means++', max_iter=300, n_clusters=nClusters, n_init=10,
                random_state=0, tol=0.0001, verbose=0).fit(array.reshape(-1, 1))
    idx = np.argsort(kmeans.cluster_centers_.sum(axis=1))
    lut = np.zeros_like(idx)
    lut[idx] = np.arange(nClusters)
    return lut[kmeans.labels_]