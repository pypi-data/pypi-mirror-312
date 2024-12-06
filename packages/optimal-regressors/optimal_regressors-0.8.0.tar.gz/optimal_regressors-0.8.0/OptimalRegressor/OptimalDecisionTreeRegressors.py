from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error

def OptimalMaxLeafNodes(candidate_nodes,trainX,trainy,valX,valy,mae):
    best_node = candidate_nodes[0]
    for i in candidate_nodes:
        model = DecisionTreeRegressor(max_leaf_nodes=i,random_state=0)
        model.fit(trainX,trainy)
        preds = model.predict(valX)
        err = mean_absolute_error(preds,valy)
        if err<mae:
            mae = err
            best_node = i
    return best_node

def OptimalMinSamplesSplit(candidate_splits,trainX,trainy,valX,valy,mae,node=5):
    best_split = candidate_splits[0]
    for i in candidate_splits:
        model = DecisionTreeRegressor(max_leaf_nodes=node,min_samples_split=i,random_state=0)
        model.fit(trainX,trainy)
        preds = model.predict(valX)
        err = mean_absolute_error(preds,valy)
        if err<mae:
            mae = err
            best_split = i
    return best_split

def OptimalMinSampleLeaf(candidate_leaves,trainX,trainy,valX,valy,mae,node=5,split=2):
    best_leaf = candidate_leaves[0]
    for i in candidate_leaves:
        model = DecisionTreeRegressor(max_leaf_nodes=node,min_samples_split=split,min_samples_leaf=i,random_state=0)
        model.fit(trainX,trainy)
        preds = model.predict(valX)
        err = mean_absolute_error(preds,valy)
        if err<mae:
            mae = err
            best_leaf = i
    return best_leaf

def OptimalMaxDepth(candidate_depth,trainX,trainy,valX,valy,mae,node=5,split=2,leaf=1):
    best_depth = candidate_depth[0]
    for i in candidate_depth:
        model = DecisionTreeRegressor(max_leaf_nodes=node,min_samples_leaf=leaf,min_samples_split=split,max_depth=i,random_state=0)
        model.fit(trainX,trainy)
        preds = model.predict(valX)
        err = mean_absolute_error(preds,valy)
        if err<mae:
            mae = err
            best_depth = i
    return best_depth

    