class Node:

    def __init__(self, nod_id, node_type, demand, balance):
        self.nod_id = nod_id
        self.node_type = node_type
        self.demand = demand
        self.balance = balance

    def positivCheck(self):
        if self.balance == 0:
            return 'green'
        else:
            return 'red'
