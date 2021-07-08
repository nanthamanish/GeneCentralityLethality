import pandas as pd
import networkx as nx
import time
import os

def get_features(G, mi=1000):
    """Function to extract features from the Graph

    Built in functions from the networkx package is used to extract the 
    following centrality measures.
        1) Degree centrality
        2) Eigenvector centrality
        3) Closeness centrality
        4) Betweenness centrality
        5) Subgraph centrality
        6) Load centrality
        7) Harmonic centrality
        8) Reaching centrality
        9) Clustering centrality
        10) Pagerank
    """

    nodes = nx.nodes(G)
    
    lrc_cen = {}
    pagerank = {}
    pre_time = time.time()
    for v in nodes:
        lrc_cen[v] = nx.local_reaching_centrality(G, v)
        pagerank[v] = 0
    
    print("Local Reaching Centrality Computed")
    print("Time taken = ",str(time.time() - pre_time), '\n')
    
    pre_time = time.time()
    voterank = nx.voterank(G)
    val=nodes.__len__()
    for v in voterank:
        pagerank[v] = val
        val-=1
    print("Page Rank Computed")
    print("Time taken = ",str(time.time() - pre_time), '\n')
    
    pre_time = time.time()
    deg_cen = nx.degree_centrality(G)
    print("Degree Centrality Computed")
    print("Time taken = ",str(time.time() - pre_time), '\n')

    pre_time = time.time()
    eig_cen = nx.eigenvector_centrality(G, max_iter=mi)
    print("Eigenvector Centrality Computed")
    print("Time taken = ",str(time.time() - pre_time), '\n')

    pre_time = time.time()
    clo_cen = nx.closeness_centrality(G)
    print("Closeness Centrality Computed")
    print("Time taken = ",str(time.time() - pre_time), '\n')

    pre_time = time.time()
    bet_cen = nx.betweenness_centrality(G)
    print("Betweenness Centrality Computed")
    print("Time taken = ",str(time.time() - pre_time), '\n')

    pre_time = time.time()
    sub_cen = nx.subgraph_centrality(G)
    print("Subgraph Centrality Computed")
    print("Time taken = ",str(time.time() - pre_time), '\n')

    pre_time = time.time()
    ld_cen = nx.load_centrality(G)
    print("Load Centrality Computed")
    print("Time taken = ",str(time.time() - pre_time), '\n')

    pre_time = time.time()
    har_cen = nx.harmonic_centrality(G)
    print("Harmonic Centrality Computed")
    print("Time taken = ",str(time.time() - pre_time), '\n')

    pre_time = time.time()
    cluster = nx.clustering(G)
    print("Clustering Coefficients computed")
    print("Time taken = ",str(time.time() - pre_time), '\n')

    df = pd.DataFrame([ deg_cen, eig_cen, clo_cen,
                        bet_cen, sub_cen, ld_cen,
                        har_cen, lrc_cen, cluster, 
                        pagerank],
                      index=["degree_centrality",
                            "eigenvector_centrality",
                            "closeness_centrality",
                            "betweenness_centrality",
                            "subgraph_centrality",
                            "load_centrality",
                            "harmonic_centrality",
                            "reaching_centrality",
                            "clustering_centrality",
                            "pagerank"])
    return df.transpose()

if __name__ == "__main__":
    with open("graphs.txt") as f:
        graphs = f.readlines()
        graphs = [x.strip() for x in graphs]

        cwd = os.getcwd()
        print(cwd)

        for i in range (0, len(graphs)):
            graphname = graphs[i]
            print(graphname)
            f_in = cwd + '\Graphs\\'+ graphname+ '.ppi.txt'
            print(f_in)
            f_out = cwd + '\Features\\' + graphname + '.csv'
            print(f_out)
            start_time = time.time()
            G = nx.read_weighted_edgelist(f_in)
            df = get_features(G)
            
            #writing to out file
            df.to_csv(f_out)
            f_t = open("time_log.txt", 'a')
            f_t.write(graphname + '\tt = ' + str(time.time() - start_time) + '\n')
        else:
            print("Wrong Argument")