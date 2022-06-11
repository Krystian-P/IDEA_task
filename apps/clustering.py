from time import time
from sklearn import metrics
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import pandas as pd
from matplotlib import pyplot as plt
import subprocess
import shlex


def clusterData(branchData):
    array = branchData[:, 2]
    km = KMeans(copy_x=True, init='k-means++', max_iter=300, n_clusters=4, n_init=10,
                random_state=0, tol=0.0001, verbose=0)
    yPredicted = km.fit_predict(array.reshape(-1, 1))
