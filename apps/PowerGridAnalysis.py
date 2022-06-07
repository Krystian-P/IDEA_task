import random
import h5py
import numpy as np
from model.DataClass import Node, Branch

hour_dict = {}

def getGridLayout():
    try:
        with h5py.File('C:/Users/Krystian/Desktop/IDEA_task/task_data.hdf5', 'r') as f:
            data = f.get('results')
            hour = data.get('hour_3')
            nodes = hour.get('nodes')
            branches = hour.get('branches')
            gridLayout = {'nodes': np.array(nodes)[:, 0:2],
                          'branches': np.array(branches)[:, 0:2]}
    except:
        print('error')
    return [gridLayout, data]


def getSpecyficData():
    hour_dict = {}
    labels = ['hour_' + str(i) for i in range(1, 25)]
    try:
        with h5py.File('task_data.hdf5', 'r') as f:
            data = f.get('results')
            for label in labels:
                x = data.get(label)
                nodes = x.get('nodes')
                gens = x.get('gens')
                branches = x.get('branches')
                hour_dict[label] = {'nodes': np.array(nodes),
                                    'gens': np.array(gens),
                                    'branches': np.array(branches)}
    except:
        print('error')
    return hour_dict


def prepNodes(gridLayout):
    node_list = createNodes(gridLayout)
    graph_nodes_list = [(str(node.nod_id), str(node.nod_id)[:-2], random.randint(0, 100), random.randint(-100, 0)) for node in
                        node_list]
    return graph_nodes_list

def createNodes(gridLayout):
    node_list = []
    for row in gridLayout:
        node = Node(row[0], row[1])
        node_list.append(node)
    return node_list

def prepBranches(gridLayout):
    branch_list = createBranches(gridLayout)
    graph_nodes_list = [(str(branch.node_from), str(branch.node_to)) for branch in
                        branch_list]
    return graph_nodes_list

def createBranches(gridLayout):
    branch_list = []
    for row in gridLayout:
        branch = Branch(row[0], row[1])
        branch_list.append(branch)
    return branch_list

