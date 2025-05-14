# Logistic regression classificator

import numpy as np

def GetDecisiveFunction(trainingDataset, gradientDescentIterations = 20000, gradientDescentRate = 0.5):
    
    POSITIVE_CLASS = 4
    NEGATIVE_CLASS = 2
    
    m = len(trainingDataset)
    
    trainingDataset = np.array(trainingDataset)
    
    w = np.array([0.0 for _ in range(9)])
    b = 0.0
    
    #Helper function
    def GetPredictedY(w, b, x):
        return 1 / (1 + np.exp(-np.dot(w, x) - b))
    
    #Gradient descent method
    for _ in range(gradientDescentIterations):
        
        w_derivative = sum((GetPredictedY(w,b,trainingDataset[i][0:9])-(1 if trainingDataset[i][9] == POSITIVE_CLASS else 0))*trainingDataset[i][0:9] for i in range(m))/m
        b_derivative = sum((GetPredictedY(w,b,trainingDataset[i][0:9])-(1 if trainingDataset[i][9] == POSITIVE_CLASS else 0)) for i in range(m))/m
        
        w -= gradientDescentRate * w_derivative
        b -= gradientDescentRate * b_derivative
    
    #Takes [x_1,x_2,...,x_9], returns (predicted class, probability of that class)
    def DecisiveFunction(X):
        if len(X) != 9:
            raise ValueError("DecisiveFunction: Wrong arguments")
        
        positiveProbability = GetPredictedY(w, b, X)
        
        if positiveProbability > 0.5:
            return POSITIVE_CLASS, positiveProbability
        else:
            return NEGATIVE_CLASS, 1-positiveProbability
        
    return DecisiveFunction

def GetLossFunctionValuesForComparation(trainingDataset, totalGradientDescentIterations = 50000, gradientDescentStep = 1000, gradientDescentRate = 0.5):
    POSITIVE_CLASS = 4
    NEGATIVE_CLASS = 2
    
    m = len(trainingDataset)
    
    trainingDataset = np.array(trainingDataset)
    
    w = np.array([0.0 for _ in range(9)])
    b = 0.0
    
    lossFunctionArray = []
    
    #Helper function
    def GetPredictedY(w, b, x):
        return 1 / (1 + np.exp(-np.dot(w, x) - b))
    
    #Gradient descent method
    for k in range(totalGradientDescentIterations):
        
        w_derivative = sum((GetPredictedY(w,b,trainingDataset[i][0:9])-(1 if trainingDataset[i][9] == POSITIVE_CLASS else 0))*trainingDataset[i][0:9] for i in range(m))/m
        b_derivative = sum((GetPredictedY(w,b,trainingDataset[i][0:9])-(1 if trainingDataset[i][9] == POSITIVE_CLASS else 0)) for i in range(m))/m
        
        w -= gradientDescentRate * w_derivative
        b -= gradientDescentRate * b_derivative
        
        if (k+1)%gradientDescentStep == 0 and k >= 5000:
            
            currentErrorFunction = -(1/m)*sum((1 if trainingDataset[i][9] == POSITIVE_CLASS else 0)*np.log(GetPredictedY(w,b,trainingDataset[i][0:9])) + (1 - 1 if trainingDataset[i][9] == POSITIVE_CLASS else 0)*(1 - np.log(GetPredictedY(w,b,trainingDataset[i][0:9]))) for i in range(m))
            
            lossFunctionArray.append(currentErrorFunction)
        
    return lossFunctionArray

def GetDecisiveFunctionWithRegularization(trainingDataset, gradientDescentIterations = 20000, gradientDescentRate = 0.5, l2_lambda = 0.01):
    
    POSITIVE_CLASS = 4
    NEGATIVE_CLASS = 2
    
    m = len(trainingDataset)
    
    trainingDataset = np.array(trainingDataset)
    
    w = np.array([0.0 for _ in range(9)])
    b = 0.0
    
    #Helper function
    def GetPredictedY(w, b, x):
        return 1 / (1 + np.exp(-np.dot(w, x) - b))
    
    #Gradient descent method
    for _ in range(gradientDescentIterations):
        
        w_derivative = (sum((GetPredictedY(w,b,trainingDataset[i][0:9])-(1 if trainingDataset[i][9] == POSITIVE_CLASS else 0))*trainingDataset[i][0:9] for i in range(m)) + l2_lambda*w)/m
        b_derivative = sum((GetPredictedY(w,b,trainingDataset[i][0:9])-(1 if trainingDataset[i][9] == POSITIVE_CLASS else 0)) for i in range(m))/m
        
        w -= gradientDescentRate * w_derivative
        b -= gradientDescentRate * b_derivative
    
    #print(f"w = {w}, b = {b}")
    
    #Takes [x_1,x_2,...,x_9], returns (predicted class, probability of that class)
    def DecisiveFunction(X):
        if len(X) != 9:
            raise ValueError("DecisiveFunction: Wrong arguments")
        
        positiveProbability = GetPredictedY(w, b, X)
        
        if positiveProbability > 0.5:
            return POSITIVE_CLASS, positiveProbability
        else:
            return NEGATIVE_CLASS, 1-positiveProbability
        
    return DecisiveFunction