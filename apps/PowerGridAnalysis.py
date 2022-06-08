import h5py
import numpy as np
import pandas as pd
from models.DataClass import Node, Branch

hour_dict = {}

def getGridLayout(hour):

    with h5py.File('C:/Users/Krystian/Desktop/IDEA_task/task_data.hdf5', 'r') as f:
        results = f.get('results')
        hour = results.get(f'hour_{hour}')
        nodes = hour.get('nodes')
        branches = hour.get('branches')
        gridLayout = {'nodes': np.array(nodes),
                      'branches': np.array(branches)}
    return [gridLayout, results]

def getHDF():
    with h5py.File('C:/Users/Krystian/Desktop/IDEA_task/task_data.hdf5', 'r') as f:
        results = f.get('results')
        node = results.get('/results/hour_1/nodes')
        data = np.array(node)
        print(data)



def prepNodes(gridLayout):
    node_list = createNodes(gridLayout)
    graph_nodes_list = [(str(node.nod_id), str(node.nod_id)[:-2], node.positiv()) for node in
                        node_list]
    return graph_nodes_list

def createNodes(gridLayout):
    node_list = []
    for row in gridLayout:
        node = Node(row[0], row[1], row[2])
        node_list.append(node)
    return node_list

def prepBranches(gridLayout):
    branch_list = createBranches(gridLayout)
    graph_nodes_list = []
    for branch in branch_list:
        if branch.flow < 0:
            temp = branch.node_from
            branch.node_from = branch.node_to
            branch.node_to = temp
            branch.flow *= -1
        graph_nodes_list.append((str(branch.node_from), str(branch.node_to), str("{:.2f}".format(branch.flow))))
    return graph_nodes_list

def createBranches(gridLayout):
    branch_list = []
    for row in gridLayout:
        branch = Branch(row[0], row[1], row[2])
        branch_list.append(branch)
    return branch_list

def nodeBalance():
    pass