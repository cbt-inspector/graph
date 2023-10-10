import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from graph import graphTester, randomColor
import time
import datetime
import sys
from PIL import Image
sys.setrecursionlimit(10000)

def test1(size, iter):
    '''## IGNORE
    average length for size 100 ~33.7s
    median length (108.5s - 9.8s) -> 59s
    
    after cluster renaming optimization:
    average length for size 100 ~ 5.5s
    median length (6.0s - 5.2s) -> 5.6s

    for comparison, old method took 12s for size 50 (25% as many nodes)
    '''
    SIZE = size
    ITERATIONS = iter
    times = []
    for x in range(ITERATIONS):
        print(f"Now testing {x}th graph")
        start = datetime.now()
        G = graphTester(SIZE)
        nx.draw(
            G.getG(),
            pos=G.generateNxPosition(),
            with_labels=False,
            width=1,
            node_size=15,
            font_size=11,
        )
        sizeSq = SIZE*SIZE

        for i in range(sizeSq):
            G.addEdge()

            '''nx.draw(
                    G.getG(),
                    pos=G.generateNxPosition(),
                    with_labels=False,
                    width=1,
                    node_size=15,
                    font_size=11,
                )'''
            print(f"{x} - {np.round(np.multiply(np.divide(i, np.square(SIZE)), 100), 2)}%             ", end='\r')
        times.append((datetime.now()-start).total_seconds())
        print(f"Time taken to completion: {times[-1]}s")

    print("")
    print(f"Average time for all tests: {sum(times)/ITERATIONS}")

def render(dpi = 350) -> str:
    '''Render current PLT figure and give it a unique name
    
    Returns the location of the rendered image'''
    uniqueID = f"cache/{time.time()}"
    plt.savefig(f"{uniqueID}.png", dpi=dpi)
    plt.savefig(f"{uniqueID}.svg", dpi=dpi)
    return uniqueID

def drawGraph(size: int, percentage: float, type: str = 'square', coloredClusters=False, edgeWidth=10) -> str:
    '''
    Draw a square graph of size:
    size with the
    percentage: percentage of possible edges added
    
    Returns the location of rendered image'''

    plt.clf()
    G = graphTester(size, type)
    G.addEdgeToPercentage(percentage)

    nodeSize = 100
    if size > 11:
        #nodeSize = pow(3.678, (-0.04*size)+3.96) + 0.25
        nodeSize = np.power(3.678, np.multiply(-0.04, size)+3.96) + 0.25
    

    if not coloredClusters:
        nx.draw(
            G.g,
            pos = G.generateNxPosition(),
            with_labels = True,
            width = edgeWidth,
            node_size = nodeSize,
            font_size = 5
        )
    else:
        position = G.generateNxPosition()
        if size > 40:
            nx.draw_networkx_edges(
                G.g,
                pos = position,
                width = edgeWidth
            )
        for ignore, x in G.clusters.items():
            if len(x) > 0:
                nx.draw_networkx_nodes(
                    G.g,
                    pos = position,
                    node_size = nodeSize,
                    nodelist = x,
                    node_color = randomColor(),
                    node_shape='s'
                )
    
    plt.title(f"Size: {size}, Type: {type}, Percentage: {percentage}\nNodes: {size*size}, Clusters: {G.numberOfClusters()}, Largest cluster len: {G.lenOflargestCluster()}")
    return render()

def drawPlot(size: int, type: str = 'square', plotType: str = 'line', edgeWidth=2) -> str:
    '''Draw PLT graph
    
    If scatter=True (default) returns a scatterplot, else returns a normal graph (line!)

    Returns the location of rendered image'''
    
    G = graphTester(size, type)
    x = []
    lenClusters = []
    lenLargestCluster = []
    for i in range(size*size):
        G.addEdge()
        x.append(i)
        lenClusters.append(G.numberOfClusters())
        lenLargestCluster.append(G.lenOflargestCluster())
        print(f"{i} - {G.numberOfClusters()}")

    fig, ax = plt.subplots()
    if plotType == 'line':
        ax.plot(x, lenClusters, color='blue', label='Number of clusters')
        ax.plot(x, lenLargestCluster, color='green', label='Length of largest cluster')
    elif plotType == 'scatter':
        ax.scatter(x, lenClusters, color='blue', label='Number of clusters', s=15)
        ax.scatter(x, lenLargestCluster, color='green', label='Length of largest cluster', s=15)
    ax.legend(loc='upper left')
    ax.set_xlabel("Number of Edges")
    
    plt.title("test")
    return render()

if __name__ == "__main__":
    G = graphTester(30, type= 'hexagonal')
    x = [] # number of edges
    y = [] # size of largest cluster
    lengthNonEdges = G.lenNonEdges()
    for i in range(lengthNonEdges):
        G.addEdge()
        x.append(lengthNonEdges - i)
        y.append(G.lenOflargestCluster())

    img = drawPlot(x, y, "Number of edges", "Size of largest cluster")
    Image.open(img).show()
    