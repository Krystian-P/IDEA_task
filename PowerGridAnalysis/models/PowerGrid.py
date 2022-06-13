import pandas as pd

from models.Gen import Gen
from models.Node import Node
from models.Branch import Branch


class PowerGrid:

    def __init__(self, dictionary, colorList, nClusters=1):
        self.nodes, self.branches, self.gens = self.createObjects(dictionary)
        self.colorList = colorList
        self.nClusters = nClusters

    def createObjects(self, dictionary):
        nodesList = self.createNodes(dictionary['nodes'])
        branchesList = self.createBranches(dictionary['branches'])
        gensList = self.createGens(dictionary['gens'])
        return [nodesList, branchesList, gensList]

    @staticmethod
    def createNodes(dictionary):
        nodeList = []
        for row in dictionary:
            if round(row[3], 3) == -0:
                row[3] = 0
            node = Node(row[0], row[1], row[2], row[3])
            nodeList.append(node)
        return nodeList

    @staticmethod
    def createBranches(dictionary):
        branchList = []
        for row in dictionary:
            branch = Branch(row[0], row[1], row[2], row[3])
            branchList.append(branch)

        return branchList

    @staticmethod
    def createGens(dictionary):
        gensList = []
        for row in dictionary:
            gen = Gen(row[0], row[1], row[2])
            gensList.append(gen)
        return gensList

    def prepNodes(self):
        graphNodesList = [(str(node.nod_id), str("{:.0f}".format(node.nod_id)), str(node.positivCheck())) for node in
                          self.nodes]
        return graphNodesList

    def prepNodeDataFrame(self):
        nodeDataFrame = [(str(node.nod_id), str("{:.2f}".format(node.balance))) for node in self.nodes]
        return nodeDataFrame

    def prepBranches(self):
        if self.nClusters == 1:
            graphBranchesList = [(str(branch.node_from), str(branch.node_to), str("{:.2f}".format(branch.flow)),
                                  'grey') for branch in self.branches]
        else:
            graphBranchesList = [(str(branch.node_from), str(branch.node_to), str("{:.2f}".format(branch.flow)),
                                  str(self.colorList[int(branch.cluster)])) for branch in self.branches]
        return graphBranchesList

    def genrationPlotGenerators(self):
        dataFrameGeneratorsList = [[str(gen.nod_id), "{:.2f}".format(gen.generation)] for gen
                                   in self.gens]
        return dataFrameGeneratorsList

    def getNodeInfo(self, nodeId):
        node = self.nodes[int(nodeId) - 1]
        noteDict = {
            "Node Id": node.nod_id,
            "Node Type": node.node_type,
            'Node Demand': "{:.2f}".format(node.demand)
        }
        return noteDict

    def clustersDataFrame(self):
        dataFrameBranchesList = [[branch.cluster, branch.flow] for branch in self.branches]
        dataFrame = pd.DataFrame(dataFrameBranchesList, columns=['cluster', 'flow'])
        groupedData = dataFrame.groupby('cluster')
        maximums = groupedData.max()
        minimums = groupedData.min()
        clusterData = minimums.merge(maximums, how='left', on='cluster')

        return clusterData.sort_values(by=['flow_x'])
