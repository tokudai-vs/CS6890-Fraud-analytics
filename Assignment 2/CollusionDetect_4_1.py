###############################################################################################

#Implementation of Shared Nearest Neighbour Graph Clustering Algorithm to Detect Collusion sets
#Contributors:
#Vishal Singh Yadav: CS20MTECH01001
#Anilava Kundu: CS20MTECH01002
#Kuldeep Gautam: CS20MTECH01004

###############################################################################################

import pandas as pd
import networkx as nx


#Creates a Map from a vertex to a cluster it is present in
def verticeToCluster(G,clusters):

    vert2Clust={}

    for u in G.nodes:
        for i in range(0,len(clusters)):
            if u in clusters[i]:
                vert2Clust[u]=clusters[i]

    return vert2Clust


#Implementation of Shared Nearest Neighbours Algorithm
def findCollusionSets(G,dict_kNN,kt):
 
    vertices=G.nodes
    
    clusters=[[x] for x in vertices]

    vert2Clust=verticeToCluster(G,clusters)

    KT=kt

    #Algorithm given in the paper
    for u in vertices:
        for v in vertices:
            l=len([value for value in dict_kNN[u] if value in dict_kNN[v]]) 
            c_u=vert2Clust[u]
            if v not in c_u and l >= KT and u in dict_kNN[v] and v in dict_kNN[u]: 
                
                c_v=vert2Clust[v]

                c_u_v=c_u+c_v


                clusters.remove(c_v)
                clusters.remove(c_u)

                clusters.append(c_u_v)

                for x in c_u_v:
                    vert2Clust[x]=c_u_v


    
    collude_set=[]
    for x in clusters:
        if(len(x)>=2):
            collude_set.append(x)

    return collude_set


#Creates a dictionary for kNN for each vertex
def find_KNN(G,k):
    
    dict_kNN={}

    for u in G.nodes:
        #Sorting neighbours in descending order according to Amount[more amount traded ===> less distance] 
        sort_dict=sorted(G[u].items(),key=lambda edge: edge[1]['Amount'],reverse=True)
        sorted_neighbours=[]
        for v in sort_dict:
            sorted_neighbours.append(v[0])
            #taking top k neighbours
            dict_kNN[u]=sorted_neighbours[0:k]
        if(len(sort_dict)==0):
            dict_kNN[u]=[]
    return dict_kNN



if __name__=="__main__":

    df=pd.read_csv('cluster.csv')
    
    Graphtype=nx.DiGraph()

    kt=2
    K=4

    G=nx.from_pandas_edgelist(df,source='Vertex 1',target='Vertex 2',edge_attr='Amount',create_using=Graphtype)
    
    dict_kNN=find_KNN(G,K)
    
    print(findCollusionSets(G,dict_kNN,kt))
