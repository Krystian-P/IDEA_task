class Branch:

    def __init__(self, node_from, node_to, flow=0):
        self.node_from = node_from
        self.node_to = node_to
        self.flow = flow