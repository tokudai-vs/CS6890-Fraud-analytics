###############################################################################################

# Implementation of Mutual Nearest Neighbour Graph Clustering Algorithm to Detect Collusion sets
# Contributors:
# Vishal Singh Yadav: CS20MTECH01001
# Anilava Kundu: CS20MTECH01002
# Kuldeep Gautam: CS20MTECH01004

###############################################################################################

import pandas as pd
import networkx as nx
import sys


#Function to calculate all K-Nearest Neighbours
def find_KNN(G, k):

    dict_kNN = {}
    for u in G.nodes:
        sort_dict = sorted(
            G[u].items(), key=lambda edge: edge[1]["Amount"], reverse=True
        )
        count = 0
        sorted_neighbours = []
        for v in sort_dict:
            if count >= k:
                G.remove_edge(u, v[0])
                continue
            count += 1
            sorted_neighbours.append(v[0])

        dict_kNN[u] = sorted_neighbours

    return dict_kNN

#Function to calculate mnv for a pair of clusters
def calculateMNV(C1, C2, dict_kNN):

    mnv_list = []
    for v1 in C1:
        for v2 in C2:
            if v2 in dict_kNN[v1] and v1 in dict_kNN[v2]:
                sum_mnv = dict_kNN[v1].index(v2) + 1 + dict_kNN[v2].index(v1) + 1
                mnv_list.append(sum_mnv)
            elif v2 in dict_kNN[v1] and v1 not in dict_kNN[v2]:
                sum_mnv = dict_kNN[v1].index(v2) + 100
                mnv_list.append(sum_mnv)
            elif v2 not in dict_kNN[v1] and v1 in dict_kNN[v2]:
                sum_mnv = dict_kNN[v2].index(v1) + 100
                mnv_list.append(sum_mnv)
            else:
                mnv_list.append(200)

    avg_mnv = sum(mnv_list) / len(mnv_list)

    return avg_mnv

#Function that implements algorithm 4.2 from the paper
def find_clusters(G, m, dict_kNN):

    vertices = G.nodes

    clusters = [[x] for x in vertices]

    min_c1 = None
    min_c2 = None

    MAX_MNV=200

    while len(clusters) > m:
        min_mnv = sys.maxsize
        for x in clusters:
            for y in clusters:
                if x == y:
                    continue
                mnv = calculateMNV(x, y, dict_kNN)
                if mnv <= min_mnv:
                    min_mnv = mnv
                    min_c1 = x
                    min_c2 = y
        
        if min_mnv >= MAX_MNV:
            break

        min_c1_c2=min_c1+min_c2
        clusters.remove(min_c1)
        clusters.remove(min_c2)
        clusters.append(min_c1_c2)
        
    print(clusters)

if __name__ == "__main__":

    df = pd.read_csv("cluster.csv")

    Graphtype = nx.DiGraph()

    kt = 2 
    K = 4 # 4 Nearest neighbours

    G = nx.from_pandas_edgelist(
        df,
        source="Vertex 1",
        target="Vertex 2",
        edge_attr="Amount",
        create_using=Graphtype,
    )

    dict_kNN = find_KNN(G, K)

    find_clusters(G, len(G.nodes)-1, dict_kNN)

