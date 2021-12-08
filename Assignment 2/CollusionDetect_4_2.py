import pandas as pd
import networkx as nx
import sys


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


def calculateMNV(C1, C2, dict_kNN):

    mnv_list = []
    for v1 in C1:
        for v2 in C2:
            if v2 in dict_kNN[v1] and v1 in dict_kNN[v2]:
                # print(v2,dict_kNN[v1])
                # print(v1,dict_kNN[v2])
                sum_mnv = dict_kNN[v1].index(v2) + 1 + dict_kNN[v2].index(v1) + 1
                # print(sum_mnv)
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


def find_clusters(G, m, dict_kNN):

    vertices = G.nodes

    clusters = [[x] for x in vertices]

    min_mnv = sys.maxsize
    min_c1 = None
    min_c2 = None

    # while len(clusters) > m:
    for x in clusters:
        for y in clusters:
            if x == y:
                continue
            mnv = calculateMNV(x, y, dict_kNN)
            if mnv <= min_mnv:
                min_mnv = mnv
                min_c1 = x
                min_c2 = y

    print(min_mnv)
    # min_c1_c2=min_c1+min_c2
    # clusters.remove(min_c1)
    # clusters.remove(min_c2)
    # clusters.append(min_c1_c2)


if __name__ == "__main__":

    df = pd.read_csv("cluster.csv")

    Graphtype = nx.DiGraph()

    kt = 2
    K = 4

    G = nx.from_pandas_edgelist(
        df,
        source="Vertex 1",
        target="Vertex 2",
        edge_attr="Amount",
        create_using=Graphtype,
    )
    # print(G.nodes)

    dict_kNN = find_KNN(G, K)

    find_clusters(G, 5, dict_kNN)

