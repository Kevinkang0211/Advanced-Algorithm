
import numpy as np
import pandas as pd

# Kruskal's algorithm in Python


class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

    # Search function

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def apply_union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    #  Applying Kruskal algorithm
    def kruskal_algo(self):
        result = []
        i, e = 0, 0
        self.graph = sorted(self.graph, key=lambda item: item[2])
        parent = []
        rank = []
        for node in range(self.V):
            parent.append(node)
            rank.append(0)
        while e < self.V - 1:
            u, v, w = self.graph[i]
            i = i + 1
            x = self.find(parent, u)
            y = self.find(parent, v)
            if x != y:
                e = e + 1
                result.append([u, v, w])
                self.apply_union(parent, rank, x, y)
        # for u, v, weight in result:
        #     print("%d - %d: %d" % (u, v, weight))
        sum_weight = 0
        for i in range(len(result)):
            sum_weight += result[i][2]
        print('The weight of',self.V , 'nodes is' ,sum_weight)
       
    
print('------MST with Kruskal algorithm(Upper triangle)------')
for k in range(10,60,10):
    g = Graph(k)
    
    data = np.array(pd.read_excel('MSTdata.xlsx'))
    data = data[:,1:]

    for i in range(k):
        for j in range(i+1,k):
            g.add_edge(i, j, data[i][j])
    g.kruskal_algo()
    
print('\n------MST with Kruskal algorithm(Lower triangle)------')
for k in range(10,60,10):
    g = Graph(k)
    
    data = np.array(pd.read_excel('MSTdata.xlsx'))
    data = data[:,1:]

    for i in range(k):
        for j in range(0,i):
            g.add_edge(i, j, data[i][j])
            
            
    g.kruskal_algo()
