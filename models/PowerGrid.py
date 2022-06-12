import pandas as pd

from models.Gen import Gen
from models.Node import Node
from models.Branch import Branch



class PowerGrid:

    def __init__(self, dictionary, nCluster, colorList):
        self.nCluster = nCluster
        self.nodes, self.branches, self.gens = self.createObjects(dictionary)
        self.colorList = colorList


    def createObjects(self, dictionary):
        nodesList = self.createNodes(dictionary['nodes'])
        branchesList = self.createBranches(dictionary['branches'])
        gensList = self.createGens(dictionary['gens'])
        return [nodesList, branchesList, gensList]

    def createNodes(self, dictionary):
        nodeList = []
        for row in dictionary:
            node = Node(row[0], row[1], row[2], row[3])
            nodeList.append(node)
        return nodeList

    def createBranches(self, dictionary):
        branchList = []
        for row in dictionary:
            branch = Branch(row[0], row[1], row[2], row[3])
            branchList.append(branch)
        return branchList

    def createGens(self, dictionary):
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
        graphBranchesList = [(str(branch.node_from), str(branch.node_to), str("{:.2f}".format(branch.flow)),
                              str(self.colorList[int(branch.cluster)])) for branch in self.branches]
        return graphBranchesList

    def costPlotGenerators(self):
        dataFrameGeneratorsList = [[str(gen.nod_id), "{:.2f}".format(gen.generation)] for gen
                                   in self.gens]
        return dataFrameGeneratorsList

    def clustersDataFrame(self):
        dataFrameBranchesList=[[branch.cluster, branch.flow] for branch in self.branches]
        dataFrame = pd.DataFrame(dataFrameBranchesList, columns=['cluster', 'flow'])
        groupedData = dataFrame.groupby('cluster')
        maximums = groupedData.max()
        minimums = groupedData.min()
        clusterData = minimums.merge(maximums, how='left', on='cluster')

        return clusterData.sort_values(by=['flow_x'])
