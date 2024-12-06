from sklearn.metrics import mean_absolute_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import OptimalDecisionTreeRegressors
import OptimalRandomForestRegressors

def OptimalDecisionTreeRegressors(trainX,trainy,valX,valy,candidate_nodes=[5,50,500,5000],candidate_splits=[i for i in range(2,11)],candidate_leaves=[i for i in range(1,6)],candidate_depths=[i for i in range(3,21)],fit=False):
    model = DecisionTreeRegressor(random_state=0)
    model.fit(trainX,trainy)
    preds = model.predict(valX)
    mae = mean_absolute_error(preds,valy)
    nodes = OptimalDecisionTreeRegressors.OptimalMaxLeafNodes(candidate_nodes,trainX,trainy,valX,valy,mae)
    split = OptimalDecisionTreeRegressors.OptimalMinSamplesSplit(candidate_splits,nodes,trainX,trainy,valX,valy,mae)
    leaves = OptimalDecisionTreeRegressors.OptimalMinSampleLeaf(candidate_leaves,split,nodes,trainX,trainy,valX,valy,mae)
    depth = OptimalDecisionTreeRegressors.OptimalMaxDepth(candidate_depths,leaves,split,nodes,trainX,trainy,valX,valy,mae)
    final_model = DecisionTreeRegressor(max_leaf_nodes=nodes,min_samples_split=split,min_samples_leaf=leaves,max_depth=depth,random_state=0)
    if fit:
        final_model.fit(trainX,trainy)
    return final_model


def OptimalRandomForestRegressor(trainX,trainy,valX,valy,candidate_nodes=[5,50,500,5000],candidate_estimators=[50,100,200,300,400,500],fit=False):
    model = RandomForestRegressor(random_state=0)
    model.fit(trainX,trainy)
    preds = model.predict(valX)
    mae = mean_absolute_error(preds,valy)
    nodes = OptimalRandomForestRegressors.OptimalMaxLeafNodes(candidate_nodes,trainX,trainy,valX,valy,mae)
    estimator = OptimalRandomForestRegressors.OptimalNEstimators(candidate_estimators,nodes,trainX,trainy,valX,valy,mae)
    strap = OptimalRandomForestRegressors.OptimalBootstrap([True,False],estimator,nodes,trainX,trainy,valX,valy,mae)
    final_model = RandomForestRegressor(max_leaf_nodes=nodes,n_estimators=estimator,bootstrap=strap,random_state=0)
    if fit:
        final_model.fit(trainX,trainy)
    return final_model