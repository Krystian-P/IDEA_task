from config import RELATIVEPATH
from apps.clustering import *
import h5py
import io


def getData(hour, nCluster=1, buffer=None):
    if not buffer:
        dirname = RELATIVEPATH
        dataSet = dirname + '\data.hdf5'
    else:
        dataSet = io.BytesIO(buffer)

    with h5py.File(dataSet, 'r') as f:
        nodes = np.array(f.get(f'/results/hour_{hour}/nodes'))
        branches = np.array(f.get(f'/results/hour_{hour}/branches'))
        gens = np.array(f.get(f'/results/hour_{hour}/gens'))

        nodes = nodeBalance(nodes, branches, gens)
        branches = branchesParse(branches, nCluster)
        dataDict = {'nodes': nodes,
                    'branches': branches,
                    'gens': gens
                    }
    return dataDict


def nodeBalance(nodeArray, branchesArray, generatorsArray):
    balance = nodeArray[:, 2] * -1
    for generator in generatorsArray:
        temp = np.where(generator[0] == nodeArray[:, 0])
        balance[temp[0]] += generator[1]

    for branch in branchesArray:
        temp_from = np.where(branch[0] == nodeArray[:, 0])
        balance[temp_from[0]] += branch[2]

        temp_to = np.where(branch[1] == nodeArray[:, 0])
        balance[temp_to[0]] -= branch[2]

    return np.c_[nodeArray, balance]


def branchesParse(branches, nCluster):
    for branch in branches:
        if branch[2] < 0:
            branch[[0, 1]] = branch[[1, 0]]
            branch[2] *= -1

    branches = np.c_[branches, clusterData(branches, nCluster)]
    return branches