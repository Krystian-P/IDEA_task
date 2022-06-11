import pandas as pd

from models.Gen import Gen
from models.Node import Node
from models.Branch import Branch

from config import COLORS

class PowerGrid:

    def __init__(self, dictionary, nCluster):
        self.nCluster = nCluster
        self.nodes, self.branches, self.gens = self.createObjects(dictionary)


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
        graphNodesList = [(str(node.nod_id), str("{:.2f}".format(node.nod_id)), str(node.positivCheck())) for node in
                          self.nodes]
        return graphNodesList

    def prepBranches(self):
        graphBranchesList = [(str(branch.node_from), str(branch.node_to), str("{:.2f}".format(branch.flow)),
                              branch.getColor(self.nCluster)) for branch in self.branches]
        return graphBranchesList

    def costPlotGenerators(self):
        dataFrameGeneratorsList = [[str(gen.nod_id), "{:.2f}".format(gen.generation)] for gen
                                   in self.gens]
        dataFrameGeneratorsList = pd.DataFrame(dataFrameGeneratorsList,
                                               columns=['Lokalizacja generatora', 'Generowana Moc']
                                               )
        return dataFrameGeneratorsList

    def nodeBalanceDataFrame(self):
        pass


