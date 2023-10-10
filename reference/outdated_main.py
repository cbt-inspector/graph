from outdated_graphs import testRandomGraph, timeDelta
import sys
import matplotlib.pyplot as plt
from datetime import datetime
sys.setrecursionlimit(10000000)
'''


data = []# 20 -- 80
iterations = 1

for i in range(61):
        data.append(testRandomGraph(50, i+20))
print(iterations)

for j in range(1):

    for i in range(61):
        data[i] += testRandomGraph(50, i+20)
    iterations += 1
    print(iterations)

for x in data:
    x = x/iterations



print("------------\n")
print(data)

'''
def longest(l):
    return max(([len(i) for i in l]))
    
def scatterPlotTest():
    x = []
    y = []

    for i in range(61):
        for j in range(10):
            listt = testRandomGraph(30, i+20)
            x.append(i+20)
            y.append(longest(listt))
    
    fig, ax = plt.subplots()
    
    ax.scatter(x, y, s=15)

    ax.set_xlabel("% Kanten entfernt")
    ax.set_ylabel("Größe des größten Clusters")
    plt.show()

if __name__ == "__main__":
    start = datetime.now()
    
    for x in range(100):
        testRandomGraph(50, x+1)
        print(x)
    
    print("-----------")
    print((datetime.now()-start).total_seconds())

# average value is 0.0505s