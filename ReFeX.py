from graphrole import RecursiveFeatureExtractor
import networkx as nx
import time
import os

if __name__ == "__main__":
    with open("graphs.txt") as f:
        graphs = f.readlines()
        graphs = [x.strip() for x in graphs]

        cwd = os.getcwd()
        print(cwd)

        for i in range(0, len(graphs)):
            """
            Calculating Recursively extracted features using graphrole package
            """
            graphname = graphs[i]
            s_t = time.time()
            print(graphname)
            f_in = cwd + '\Graphs\\'+ graphname+ '.ppi.txt'
            print(f_in)
            f_out = cwd + '\ReFeX\\' + graphname + '.csv'
            print(f_out)
            G = nx.read_weighted_edgelist(f_in)
            feature_ext = RecursiveFeatureExtractor(G)
            features = feature_ext.extract_features()

            #writing to out file
            features.to_csv(f_out)
            print("Time taken =", str(time.time() - s_t), sep=' ')
            print(i,"done",sep=' ',end='\n')
            pass
