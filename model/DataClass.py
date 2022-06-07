from dataclasses import dataclass


class Node:

    def __init__(self, nod_id, node_type, demand=0):
        self.nod_id = nod_id
        self.node_type = node_type
        self.demand = demand


class Gen:

    def __init__(self, nod_id, generation, cost):
        self.nod_id = nod_id
        self.generation = generation
        self.cost = cost


class Branch:

    def __init__(self, node_from, node_to, flow=0):
        self.node_from = node_from
        self.node_to = node_to
        self.flow = flow