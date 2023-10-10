import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
#import concurrent.futures as cf
#from threading import Thread
import random
#from time import sleep

# Create square lattice graph 
def createLattice(size=2):
    g = nx.Graph()
    nodeNum = 0
    nodes = []

    # Add nodes to graph and to a 2d Array
    print("Creating Nodes..")
    for x in range(size):
        nodes.append([])
        for y in range(size):
            g.add_node(nodeNum)
            nodes[x].append(nodeNum)
            nodeNum += 1

    # Create horizontal edges
    print("Done\nAdding horizontal edges..")
    for x in range(size):
        for y in range(size-1):
            g.add_edge(
                nodes[x][y],
                nodes[x][y+1]
            )
    
    # Create vertical edges
    print("Done\nAdding vertical edges..")
    for x in range(size-1):
        for y in range(size):
            g.add_edge(
                nodes[x][y],
                nodes[x+1][y]
            )
    print("Done")
    return g

def arrangeNodes(size, distance=1):
    position = {}
    nodeNum = 0
    for y in range(size):
        for x in range(size):
            position[nodeNum] = [np.multiply(x, distance), np.multiply(y, distance)]
            nodeNum += 1
    
    return position

def arrangeDefaultGrid(m: int , n: int, distance=1, invert_y=False):
    invert = 1
    if invert_y:
        invert = -1
    pos = {}
    for x in range(m):
        for y in range(n):
            pos[(x, y)] = [np.multiply(x, distance), np.multiply(np.multiply(y, invert), distance)]
    return pos

def timeDelta(start):
    return (datetime.now()-start).total_seconds()
        
# Percentage of edges to be removed
def percolate(Graph, percentage):
    edges = list(Graph.edges)
    graph = Graph
    startEdges = len(edges);currentEdges = startEdges

    while np.divide(currentEdges, startEdges) > (100-percentage)/100:
        randomInt = np.random.randint(0, currentEdges)
        
        graph.remove_edge(
            edges[randomInt][0],
            edges[randomInt][1]
        )
        edges.pop(randomInt)
        currentEdges -= 1

    return graph

def findClusters(graph):
    nodes = list(graph.nodes)
    clusters = []

    def depthSearch(node):
        clusters[-1].append(node)
        nodes.remove(node)
        a = list(nx.all_neighbors(graph, node))
        for x in a:
            if nodes.__contains__(x):
                depthSearch(x)

    while len(nodes) > 0:
        clusters.append([])
        depthSearch(nodes[0])

    return clusters

def randomColor() -> str:
    '''Returns random hexadecimal color'''
    return "#"+"".join([random.choice('0123456789abcdef') for i in range(6)])

def main():
    width, height = 30, 30

    total, t1 = datetime.now(), datetime.now()
    print("Creating graph..")

    g = nx.grid_2d_graph(width, height)
    
    print(f"Done. Took {timeDelta(t1)} seconds\nPercolating graph..")
    t1 = datetime.now()
    """
    nx.draw(
        g, 
        pos=arrangeDefaultGrid(width, height), 
        with_labels=True, 
        node_size=0.5, 
        width= 0.3, 
        font_size=0.05
    )"""
    g = percolate(g, 50)

    print(f"Done. Took {timeDelta(t1)} seconds\nArranging grid..")
    t1 = datetime.now()

    position = arrangeDefaultGrid(width, height)
    #position = nx.random_layout(g)

    print(f"Done. Took {timeDelta(t1)} seconds\nDrawing graph..")
    t1 = datetime.now()

    nx.draw_networkx_edges(
        g,
        pos=position,
        width=0.1
    )
    print(f"Done. Took {timeDelta(t1)} seconds\nRendering graph..")
    t1 = datetime.now()

    plt.savefig("30x30.png", dpi=250)

    print(f"Done. Took {timeDelta(t1)} seconds")
    print(f"Total runtime: {timeDelta(total)} seconds")

def testRandomGraph(size, percolationPercentage):
    g = nx.grid_2d_graph(size, size)
    g = percolate(g, percolationPercentage)
    return findClusters(g)

if __name__ == "__main__":
    deltaT = datetime.now()

    def printTime(nextOp, first=False):
        global deltaT
        if first:
            print(nextOp)
        else:
            print(f"Done. Took {timeDelta(deltaT)}s\n{nextOp}")
        deltaT = datetime.now()

    printTime("Creating Graph..", first=True)
    size = 20
    g = nx.grid_2d_graph(size, size)

    printTime("Running percolation algorithm..")
    g = percolate(g, 60)

    printTime("Calculating clusters..")
    clusters = findClusters(g)

    printTime("Arranging grid..")
    position = arrangeDefaultGrid(size, size)

    printTime("Drawing graph..")
    for cluster in clusters:
        nx.draw_networkx_nodes(
            g,
            pos=position,
            nodelist=cluster,
            node_size=70,
            node_color=randomColor(),
            node_shape='o'
        )

    
    nx.draw(
        g,
        pos=position,
        with_labels=False,
        width=1,
        node_size=0,
        font_size=11,
    )

    printTime("Rendering graph..")
    #plt.savefig("img/aaaaaa.png", dpi=350)
    #print(f"\nClusters: {len(clusters)}\n")
    plt.show()
    printTime("")
