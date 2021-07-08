import pandas as pd
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, f1_score, roc_auc_score, accuracy_score

with open("graphs.txt") as f:
    graphs = f.readlines()
    graphs = [x.strip() for x in graphs]

    # statistics and feature importance
    stats = pd.DataFrame(columns=['accuracy', 'precision', 'f1_score', 'auroc'])
    feat_importance = pd.DataFrame(columns=['degree_centrality', 'eigenvector_centrality',
                                            'closeness_centrality', 'betweenness_centrality',
                                            'subgraph_centrality', 'load_centrality',
                                            'harmonic_centrality', 'reaching_centrality',
                                            'clustering_centrality', 'pagerank', 'degree(mean)',
                                            'degree(mean)(mean)', 'external_edges',
                                            'external_edges(mean)', 'internal_edges'])

    # leave one out validation
    for leftout_graph in graphs:

        # Constructing training data and test data
        X_train = pd.DataFrame()
        y_train = pd.DataFrame()
        X_test = pd.DataFrame()
        y_test = pd.DataFrame()

        for graph in graphs:
            if graph != leftout_graph:
                df = pd.read_csv('Features/feat_' + graph + '.csv', index_col='index')
                X_train = X_train.append(df)
                df = pd.read_csv('EssGenes/ess_' + graph + '.csv', index_col='index')
                y_train = y_train.append(df)

        X_test = pd.read_csv('Features/feat_' + leftout_graph + '.csv', index_col='index')
        y_test = pd.read_csv('EssGenes/ess_' + leftout_graph + '.csv', index_col='index')
        y_train = list(y_train.ess)
        y_test = list(y_test.ess)

        # Scaling the features
        X_train_cols = list(X_train.columns)
        X_test_cols = list(X_test.columns)
        scaler = StandardScaler().fit(X_train.values)

        X_train = pd.DataFrame(scaler.transform(X_train.values), columns=X_train_cols)
        X_test = pd.DataFrame(scaler.transform(X_test.values), columns=X_test_cols)

        # training a XgBoost Classifier on the train set
        model = XGBClassifier()
        model.fit(X_train, y_train)

        # predicting on test set
        y_pred = model.predict(X_test)

        # keeping track of stats and feature importances
        stats.loc[len(stats.index)] = [accuracy_score(y_test, y_pred), precision_score(y_test, y_pred),
                                    f1_score(y_test, y_pred), roc_auc_score(y_test, y_pred)]
        
        # plotting importance of each feature
        feat_importance.loc[len(feat_importance.index)] = model.feature_importances_

    # ploting mean of feature importances
    feat_importance.mean().plot(kind='bar')

    # printing statistics
    print(stats.describe().iloc[1:])