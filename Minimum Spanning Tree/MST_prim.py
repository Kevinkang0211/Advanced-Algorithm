# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 17:32:29 2020

@author: kevin
"""

# Prim's Algorithm in Python


import numpy as np
import pandas as pd



def prim():
    
    INF = 9999999
    # number of vertices in graph
    V = k
    # create a 2d array of size k*k
    # for adjacency matrix to represent graph
    G = data_list
    
    
    # create a array to track selected vertex
    # selected will become true otherwise false
    selected = [0]*V
    # set number of edge to 0
    no_edge = 0
    # the number of egde in minimum spanning tree will be
    # always less than(V - 1), where V is number of vertices in
    # graph
    # choose 0th vertex and make it true
    selected[0] = True
    # print for edge and weight
    #print("Edge : Weight\n")
    selected_edge=[]
    
    while (no_edge < V - 1):
        # For every vertex in the set S, find the all adjacent vertices
        #, calculate the distance from the vertex selected at step 1.
        # if the vertex is already in the set S, discard it otherwise
        # choose another vertex nearest to selected vertex  at step 1.
        minimum = INF
        x = 0
        y = 0
        for i in range(V):
            if selected[i]:
                for j in range(V):
                    if ((not selected[j]) and G[i][j]):  
                        # not in selected and there is an edge
                        if minimum > G[i][j]:
                            minimum = G[i][j]
                            x = i
                            y = j
        #print(str(x) + "-" + str(y) + ":" + str(G[x][y]))
        
        selected_edge += [G[x][y]]
        selected[y] = True
        no_edge += 1
    
    
    print('The weight of',k,'nodes is:' , sum(selected_edge))
    


print('------MST with Prim algorithm(Upper triangle)------')
for k in range(10,60,10):
    data = np.array(pd.read_excel('MSTdata.xlsx'))
    data = data[:k,1:k+1]
    
    for i in range(k):
        for j in range(k):
            if j<i:
                data[i][j] = data[j][i]
    data_list = data[:k,:k+1]    
    #print(data_list)
    
    prim()

   
print('\n------MST with Prim algorithm(Lower triangle)------') 
for k in range(10,60,10):
    data = np.array(pd.read_excel('MSTdata.xlsx'))
    data = data[:k,1:k+1]
    
    for i in range(k):
        for j in range(k):
            if j>i:
                data[i][j] = data[j][i]
    data_list = data[:k,:k+1]    
    #print(data_list)
    
    prim()