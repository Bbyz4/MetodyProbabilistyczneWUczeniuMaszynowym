#
#
#

import numpy as np
from scipy.optimize import minimize
from sklearn.svm import SVC

def GetDecisiveFunction(trainingDataset, kernelFunction, C):
    
    X_train = np.array([record[:-1] for record in trainingDataset])
    y_train = np.array([record[-1] for record in trainingDataset]).astype(float)

    N = len(trainingDataset)

    K = np.array([np.array([kernelFunction(X_train[i], X_train[j]) for j in range(N)]) for i in range(N)])

    def W(alpha):
        alpha = np.array(alpha)
        return float(-1) * (np.sum(alpha) - 0.5 * alpha @ np.diag(y_train) @ K @ np.diag(y_train) @ alpha)
    
    EqualityConstraint = {
        'type': 'eq',
        'fun': lambda alpha: np.sum(alpha * y_train)
    }
    Bounds = [(0, C)] * N
    
    initialAlpha = np.zeros(N)

    result = minimize(W, initialAlpha, constraints=[EqualityConstraint], bounds=Bounds)
    alpha = result.x

    supportVectorIndexes = [i for i in range(N) if alpha[i] > 1e-5]
    
    b = 0
    for s in supportVectorIndexes:
        b += (y_train[s] - sum(alpha[i]*y_train[i]*K[i][s] for i in supportVectorIndexes))
    if len(supportVectorIndexes) > 0:
        b /= len(supportVectorIndexes)

    def DecisiveFunction(X):
        if len(X) != 30:
            raise ValueError("DecisiveFunction: wrong arguments")
        
        prediction = sum(alpha[i]*y_train[i]*kernelFunction(X_train[i], X) for i in supportVectorIndexes)
        
        return 1 if prediction >= 0 else -1

    return DecisiveFunction
       
def GetDecisiveFunctionUsingSKLearn(trainingDataset, kernelFunction, C):
    
    X_train = np.array([record[:-1] for record in trainingDataset])
    y_train = np.array([record[-1] for record in trainingDataset]).astype(float) 
    
    model = SVC(kernel=kernelFunction.kernelType, C=C, degree=kernelFunction.degree, gamma=kernelFunction.gamma, coef0=kernelFunction.coef0)
    model.fit(X_train, y_train)
    
    def DecisiveFunction(X):
        if len(X) != 30:
            raise ValueError("DecisiveFunction: wrong arguments")
        
        X_np = np.array(X).reshape(1, -1)
        prediction = model.predict(X_np)[0]
        
        return 1 if prediction > 0 else -1

    return DecisiveFunction
        
def CalcAccuracy(dataset, decFunc):
    score = 0
    for record in dataset:
        X_val = record[:-1]
        y_val = record[-1]
        pred = decFunc(X_val)
        if pred == y_val:
            score += 1
    
    return score / len(dataset)
        
def GetDecisiveFunctionWithValidation(trainingDataset, validatingDataset, kernelFunction):
    
    potentialCvalues = [0.0001, 0.001, 0.01, 0.1, 1, 10, 100]
    LOOP_ITERATIONS = 3
    
    currentBestDecFunc = None
    currentBestAccuracy = 0.0
    currentBestC = None
    
    for zz in range(LOOP_ITERATIONS):
        print(f"SVM: iteration {zz+1} of {LOOP_ITERATIONS}")
        
        for C in potentialCvalues:
            decFunc = GetDecisiveFunction(trainingDataset, kernelFunction, C)
            decFuncAccuracy = CalcAccuracy(validatingDataset, decFunc)
            
            if decFuncAccuracy > currentBestAccuracy:
                currentBestAccuracy = decFuncAccuracy
                currentBestDecFunc = decFunc
                currentBestC = C
                
        newCrange = np.linspace(currentBestC / 2, currentBestC * 2, 7)
        potentialCvalues = newCrange.tolist()
        
    return currentBestDecFunc
            