class PowerGrid():

    def __init__(self, dictionary):
        self.nodes, self.branches, self.gens = self.createObjects(dictionary)

    def createObjects(self, dictionary):
        return [0, 0, 0]