import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from datetime import datetime

class node:
    def __init__(self, pos: tuple, clusterId: int = 0) -> None:
        self.POS = pos
        self.clusterId = clusterId

    def __eq__(self, __value: object) -> bool:
        '''Only evaluates if the POS variable of
        two nodes are the same
        
        cluster id doesn't matter'''
        if __value.__class__ == node and self.POS == __value.POS:
            return True
        else:
            return False
        
    def __hash__(self) -> int:
        return hash(self.POS)
    
    def __str__(self) -> str:
        return f"<node_POS:{self.POS}_clusterId:{self.clusterId}>"

    def __repr__(self) -> str:
        return f"<node_POS:{self.POS}_clusterId:{self.clusterId}>"
        
class listDict:
    def __init__(self, nodes: list) -> None:
        self.list = nodes
        self.dict = {
            node.POS : node for node in self.list
        }

    def __getitem__(self, item) -> node:
        if item is int:
            return self.list[item]
        elif item is tuple:
            return self.dict[item]
        
    def __repr__(self) -> str:
        return str(self.dict)

    def clusterId(self, node: tuple) -> int:
        return self.dict[node].clusterId
    
    def find(self, pos: tuple) -> node:
        return self.dict[pos]

def allPossibleEdges(size: int, type: int =4) -> list:
    '''Returns a list of all edges that a 2d grid graph of the size:
    size could have
    
    Types:

    3-> Triangular

    4 -> Square
    
    6 -> Hexagonal'''
    if type == 4:
        return list(nx.grid_2d_graph(size, size).edges)
    elif type == 3:
        #return list(nx.triangular_lattice_graph(size, size).edges)
        temp = list(nx.grid_2d_graph(size, size).edges)
        #print(temp)
        for i in range(size-1):
            for j in range(size-1):
                temp.append((
                    (i, j), (i+1, j+1)
                ))
        #print(temp)
        return temp
    elif type == 6:
        #return list(nx.hexagonal_lattice_graph(size, size).edges)
        temp = list(nx.grid_2d_graph(size, size).edges)
        return []
    else:
        return []
def allPossibleNodes(size: int, type: int =4) -> list:
    '''Returns a list of all node that a 2d grid graph of the size:
    size could have
    
    Types:
    
    3-> Triangular
    
    4 -> Square
    
    6 -> Hexagonal'''
    if type > 2:
        return list(nx.grid_2d_graph(size, size).nodes)
    else:
        return []
    '''elif type == 3:
        return list(nx.triangular_lattice_graph(size, size).nodes)
    elif type == 6:
        return list(nx.hexagonal_lattice_graph(size, size).nodes)'''
    
def randomColor() -> str:
    '''Returns random hexadecimal color'''
    return "#"+"".join([random.choice('0123456789abcdef') for i in range(6)])

class graphTester:
    def __init__(self, size: int, type: str = 'square') -> None:
        '''Wrapper for testing graphs with bond percolation
        
        Type can be:
        
        "square"
        
        "triangular"
        
        "hexagonal"
        '''
        self.g = nx.Graph()
        if type == 'triangular':
            self.TYPE = 3
        elif type == 'hexagonal':
            self.TYPE = 6
        else:
            self.TYPE = 4
        self.SIZE = size
        self.nodes = listDict(
            [node(item, i) for i, item in enumerate(allPossibleNodes(self.SIZE, self.TYPE))]
        )
        self.g.add_nodes_from(self.nodes.list)
        self.nonEdges = allPossibleEdges(self.SIZE, self.TYPE)
        self.clusters = {
            i: [node] for i, node in enumerate(self.nodes.list)
        }

    def numberOfClusters(self) -> int:
        val = 0
        for x in self.clusters:
            if len(self.clusters[x]) > 0:
                val += 1
        return val
    
    def lenOflargestCluster(self) -> int:
        id = 0
        for x in self.clusters:
            if len(self.clusters[x]) > len(self.clusters[id]):
                id = x
        return len(self.clusters[id])

    def lenNonEdges(self) -> int:
        return len(self.nonEdges)
    
    def addEdge(self) -> None:
        '''Randomly adds an edge from a list of edges that don't yet exist,
        recalculating the clusters each time
        '''
        newEdge = random.choice(self.nonEdges)
        self.nonEdges.remove(newEdge)
        self.g.add_edge(self.nodes.find(newEdge[0]), self.nodes.find(newEdge[1]))

        def largerCluster(id1: int, id2: int) -> int:
            if len(self.clusters[id1]) > len(self.clusters[id2]):
                return id1
            else:
                return id2

        def renameCluster(node: node, newClusterId: int) -> None:
            self.clusters[node.clusterId].remove(node)
            self.clusters[newClusterId].append(node)
            node.clusterId = newClusterId
            neighbors = list(nx.all_neighbors(self.g, node))
            for neighbor in neighbors:
                if neighbor.clusterId != newClusterId:
                    renameCluster(neighbor, newClusterId)
        # self.nodes.dict[newEdge[0]].clusterId
        renameCluster(
            self.nodes.find(newEdge[1]),
            largerCluster(
                self.nodes.find(newEdge[0]).clusterId,
                self.nodes.find(newEdge[1]).clusterId
            )
        )
    
    def addEdgeToPercentage(self, percentage: float) -> None:
        '''## Add edges to given percentage

        Only works if the graph doesn't have any edges yet

        value of percentage should be between 0 - 100 (duh)
        '''
        recursions = int(np.rint([(percentage/100)*len(self.nonEdges)])[0])
        for i in range(recursions):
            self.addEdge()
    
    def generateNxPosition(self) -> dict:
        return {
            node: [node.POS[0], node.POS[1]] for node in self.nodes.list
        }

    def getG(self) -> nx.Graph:
        return self.g

if __name__ == "__main__":
    '''
    SIZE = 7
    
    nodes = listDict(
        [node(item, i) for i, item in enumerate(allPossibleNodes(SIZE))]
    )
    
    g = nx.Graph()
    g.add_nodes_from(nodes.list)

    nonEdges = allPossibleEdges(SIZE)

    clusters = {
        i: [node] for i, node in enumerate(nodes.list)
    }

    def addEdge() -> None:
        newEdge = random.choice(nonEdges)
        nonEdges.remove(newEdge)
        g.add_edge(nodes.find(newEdge[0]), nodes.find(newEdge[1]))

        def renameCluster(node: node, newClusterId: int) -> None:
            clusters[node.clusterId].remove(node)
            clusters[newClusterId].append(node)
            node.clusterId = newClusterId
            neighbors = list(nx.all_neighbors(g, node))
            for neighbor in neighbors:
                if neighbor.clusterId != newClusterId:
                    renameCluster(neighbor, newClusterId)

        renameCluster(nodes.find(newEdge[1]), nodes.dict[newEdge[0]].clusterId)
        
    def numberOfClusters() -> int:
        val = 0
        for x in clusters:
            if len(clusters[x]) > 0:
                val += 1
        return val

    def lenOflargestCluster() -> int:
        id = 0
        for x in clusters:
            if len(clusters[x]) > len(clusters[id]):
                id = x
        return len(clusters[id])

    while len(nonEdges) > 0:
        print(f"Amount of clusters: {numberOfClusters()} - Size of largest: {lenOflargestCluster()}")
        addEdge()

    
    position = {
        node: [node.POS[0], node.POS[1]] for node in nodes.list
    }
    
    nx.draw(
        g,
        pos=position,
        with_labels=False,
        width=1,
        node_size=15,
        font_size=11,
    )
    plt.show()'''
    g = graphTester(3)