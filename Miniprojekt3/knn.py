#
#
#

import numpy as np
import math

def CalcAccuracy(dataset, decFunc):
    dataset = np.array(dataset)
    X_vals = dataset[:, :-1]
    y_vals = dataset[:, -1]
    predictions = np.array([decFunc(x) for x in X_vals])
    score = (predictions == y_vals).sum()
            
    return score / len(dataset)

def GetDecisiveFunction(trainingDataset, k, distanceFunc):
    
    X_train = np.array([record[:-1] for record in trainingDataset])
    y_train = np.array([record[-1] for record in trainingDataset]).astype(float)
    
    def DecisiveFunction(X):
        if len(X) != 30:
            raise ValueError("DecisiveFunction: wrong arguments")
        
        X = np.array(X)
        
        distances = distanceFunc(X_train, X)
        
        distanceLabels = np.column_stack((distances, y_train))
        
        labelsSorted = distanceLabels[np.argsort(distances)]
        
        knearestLabels = labelsSorted[:k, 1]
        
        posCount = np.sum(knearestLabels == 1)
        negCount = k - posCount
        
        return 1 if posCount > negCount else -1
    
    return DecisiveFunction

def GetDecisiveFunctionWithValidation(trainingDataset, validatingDataset, distanceFunc):
    potentialKValues = [i for i in range(1, 7, 2)]
    
    currentBestDecFunc = None
    currentBestAccuracy = 0.0
    currentBestK = None
    
    for zz, K in enumerate(potentialKValues):
        print(f"POTENTIAL K {zz+1} out of {len(potentialKValues)}")
        
        decFunc = GetDecisiveFunction(trainingDataset, K, distanceFunc)
        decFuncAccuracy = CalcAccuracy(validatingDataset, decFunc)
        
        if decFuncAccuracy > currentBestAccuracy:
                currentBestAccuracy = decFuncAccuracy
                currentBestDecFunc = decFunc
                currentBestK = K
                
    print(f"BEST K: {currentBestK}")
    return currentBestDecFunc
        
        