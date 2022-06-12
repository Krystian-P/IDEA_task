import numpy as np
from sklearn.cluster import KMeans



def clusterData(branchData, nClusters):
    array = branchData[:, 2]
    km = KMeans(copy_x=True, init='k-means++', max_iter=300, n_clusters=nClusters, n_init=10,
                random_state=0, tol=0.0001, verbose=0)
    yPredicted = km.fit_predict(array.reshape(-1, 1))


    return np.array(yPredicted)
