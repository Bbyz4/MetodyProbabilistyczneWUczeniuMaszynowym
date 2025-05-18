#
#
#

import numpy as np

def CalcAccuracy(dataset, decFunc): #todo later: add this to utility.py
    dataset = np.array(dataset)
    X_vals = dataset[:, :-1]
    y_vals = dataset[:, -1]
    predictions = np.array([decFunc(x) for x in X_vals])
    score = (predictions == y_vals).sum()
            
    return score / len(dataset)

def EvaluateStumpWeighted(stump, X, y_real, weights):
    y_stumped = np.array([stump(x) for x in X])
    return np.sum(weights[y_real != y_stumped]) / np.sum(weights)

def GetSimpleStumpFunction(featureID, threshold, bigger):
    
    def DecisiveFunction(X):
            if len(X) != 30:
                raise ValueError("DecisiveFunction: wrong arguments")
            
            if bigger:
                return 1 if X[featureID] >= threshold else -1
            else:
                return 1 if X[featureID] <= threshold else -1
        
    return DecisiveFunction

def GetDecisiveFunction(trainingDataset, estimatorNumber):
    
    trainingDataset = np.array(trainingDataset)
    X_train = trainingDataset[:, :-1]
    y_train = trainingDataset[:, -1]
    
    m = len(trainingDataset)
    weights = np.full(m, (1/m))
    
    estimators = []
    estimatorWeights = []
    
    #DATA IS NOT SCALED HERE
    potentialNewStumps = [GetSimpleStumpFunction(i, 0, True) for i in range(21)] + [GetSimpleStumpFunction(i, 0, True) for i in range(21,29)] + [GetSimpleStumpFunction(i, -1, True) for i in range(21,29)] + [GetSimpleStumpFunction(29, 1, True)]
    potentialNewStumps += [GetSimpleStumpFunction(i, 0, False) for i in range(21)] + [GetSimpleStumpFunction(i, 0, False) for i in range(21,29)] + [GetSimpleStumpFunction(i, -1, False) for i in range(21,29)] + [GetSimpleStumpFunction(29, 1, False)]
    
    for zz in range(estimatorNumber):
        print(f"ADA: iteration {zz+1} in {estimatorNumber}")
        
        bestStump = None
        minError = float('inf')
        
        for stump in potentialNewStumps:
            error = EvaluateStumpWeighted(stump, X_train, y_train, weights)
            if(error < minError):
                bestStump = stump
                minError = error
        
        y_stumped = np.array([bestStump(X) for X in X_train])
        
        epsilon = minError
        alpha = 0.5 * max(np.log((1-epsilon)/epsilon), 0)
        
        estimators.append(bestStump)
        estimatorWeights.append(alpha)
        
        weights *= np.exp(-alpha * y_train * y_stumped)
        weights /= np.sum(weights)
        
    def DecisiveFunction(X):
        if len(X) != 30:
            raise ValueError("DecisiveFunction: wrong arguments")
        
        prediction = 0
        for i in range(len(estimators)):
            prediction += estimatorWeights[i] * estimators[i](X)
            
        return 1 if prediction > 0 else -1
    
    return DecisiveFunction