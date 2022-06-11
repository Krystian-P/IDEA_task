import h5py
import numpy as np
from apps.clustering import *
from models.Node import Node
from models.Branch import Branch
from models.Gen import Gen
from models.PowerGrid import PowerGrid

def getData(hour):
    with h5py.File('C:/Users/Krystian/Desktop/IDEA_task/task_data.hdf5', 'r') as f:

        nodes = np.array(f.get(f'/results/hour_{hour}/nodes'))
        branches = np.array(f.get(f'/results/hour_{hour}/branches'))
        gens = np.array(f.get(f'/results/hour_{hour}/gens'))

        nodes = nodeBalance(nodes, branches, gens)
        branches = branchesParse(branches)
        clusterData(branches)
        dataDict = {'nodes': nodes,
                    'branches': branches,
                    'gens': gens
                    }

        #return dataDict
        return createObjects(dataDict)


def createObjects(dataDict):
    nodesList = createNodes(dataDict['nodes'])
    branchesList = createBranches(dataDict['branches'])
    gensList = createGens((dataDict['gens']))
    return PowerGrid[nodesList, branchesList, gensList]


def createNodes(dataList):
    nodeList = []
    for row in dataList:
        node = Node(row[0], row[1], row[2], row[3])
        nodeList.append(node)
    return nodeList


def createBranches(dataList):
    branchList = []
    for row in dataList:
        branch = Branch(row[0], row[1], row[2])
        branchList.append(branch)
    return branchList


def createGens(dataList):
    gensList = []
    for row in dataList:
        gen = Gen(row[0], row[1], row[2])
        gensList.append(gen)
    return gensList


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


def branchesParse(branches):
    for branch in branches:
        if branch[2] < 0:
            branch[[0, 1]] = branch[[1, 0]]
            branch[2] *= -1
    return branches


def prepNodes(nodesList):
    graph_nodes_list = [(str(node.nod_id), str("{:.2f}".format(node.nod_id)), str(node.positivCheck())) for node in
                        nodesList]
    return graph_nodes_list


def prepBranches(branchesList):
    graph_nodes_list = []
    for branch in branchesList:
        graph_nodes_list.append((str(branch.node_from), str(branch.node_to), str("{:.2f}".format(branch.flow))))
    return graph_nodes_list

