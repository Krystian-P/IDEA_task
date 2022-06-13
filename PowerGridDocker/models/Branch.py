

class Branch:

    def __init__(self, node_from, node_to, flow=0, cluster=0):
        self.node_from = node_from
        self.node_to = node_to
        self.flow = flow
        self.cluster = cluster

    # def getColor(self, nCluster):
    #     if nCluster <= 1:
    #         return 'grey'
    #     else:
    #         return COLORS[int(self.cluster)-1]
