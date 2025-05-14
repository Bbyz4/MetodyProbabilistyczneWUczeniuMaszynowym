# Naive binary bayes classificator

import math
import numpy as np

def GetDecisiveFunction(trainingDataset, laplaceSmoothingCoefficient):
    
    presentClasses = list({record[9] for record in trainingDataset})
    
    if len(presentClasses) < 2:
        raise ValueError("naive_bayes: Too few classes are present in the training dataset")
    
    
    #priorProbabilities[y]
    #p(y==?)
    priorProbabilities = {y : (len([record for record in trainingDataset if record[9] == y])/len(trainingDataset)) for y in presentClasses}
    
    
    #conditionalProbabilities[j][k][y]
    #p(x_j==k+1|y==?)
    conditionalProbabilities = [[{y : ((len([record for record in trainingDataset if (record[j] == k and record[9] == y)]) + laplaceSmoothingCoefficient)/(len([record for record in trainingDataset if record[9] == y]) + 10*laplaceSmoothingCoefficient)) for y in presentClasses} for k in range(1,11)] for j in range(9)]
        
    #Takes [x_1,x_2,...,x_9], returns (predicted class, probability of that class)
    def DecisiveFunction(X):
        
        if len(X) != 9:
            raise ValueError("DecisiveFunction: Wrong arguments")
        
        calculatedClassProbabilities = {y: (priorProbabilities[y] * math.prod(conditionalProbabilities[j][X[j]-1][y] for j in range(9))) for y in presentClasses}
        
        totalProb = sum(calculatedClassProbabilities.values())
        
        maxProb = max(calculatedClassProbabilities.values())/totalProb
        
        bestClass = max(calculatedClassProbabilities, key=calculatedClassProbabilities.get)
        
        return bestClass, maxProb
        
    return DecisiveFunction

def GetDecisiveFunctionWithCrossValidation(trainingDataset, laplaceSmoothingMin=0.0001, laplaceSmoothingMax=3, laplaceSmoothingIterations=10):
    
    presentClasses = list({record[9] for record in trainingDataset})
    
    if len(presentClasses) < 2:
        raise ValueError("naive_bayes: Too few classes are present in the training dataset")
    
    possibleCoeffs = np.logspace(np.log10(laplaceSmoothingMin), np.log10(laplaceSmoothingMax), num=9)
    
    NUM_FOLDS = min(5, len(trainingDataset))
    FOLD_SIZE = len(trainingDataset) // NUM_FOLDS
    INFINITY = 1000
    
    for _ in range(laplaceSmoothingIterations):
        
        #print(f"POSSIBLE COEFFS: {possibleCoeffs}")
        
        bestCoeff = None
        bestAccuracy = INFINITY #enough, because dasaset has only like 600 records
        
        for coeff in possibleCoeffs:
            
            accuracies = []
        
            for i in range(NUM_FOLDS):
                
                test_set_start = i*FOLD_SIZE
                test_set_end = ((i+1)*FOLD_SIZE if i<NUM_FOLDS-1 else len(trainingDataset))
                
                test_fold = trainingDataset[test_set_start:test_set_end]
                train_fold = trainingDataset[:test_set_start] + trainingDataset[test_set_end:]
                
                try:
                    dec_func = GetDecisiveFunction(train_fold, coeff)
                except ValueError:
                    accuracies.append(INFINITY)
                    continue
                
                totalLoss = 0
            
                for record in test_fold:
                    predictedClass, probability = dec_func(record[0:9])
                    
                    if(predictedClass == record[9]):
                        totalLoss += 1-probability
                    else:
                        totalLoss += probability
                
                accuracies.append(totalLoss)
            
            coeffAccuracy = np.mean(accuracies)
            if coeffAccuracy < bestAccuracy:
                bestCoeff = coeff
                bestAccuracy = coeffAccuracy
                
                
        possibleCoeffs = list(possibleCoeffs)
        bestCoeffIndex = possibleCoeffs.index(bestCoeff)
        prevCoeff = possibleCoeffs[max(bestCoeffIndex-1, 0)]
        nextCoeff = possibleCoeffs[min(bestCoeffIndex+1, len(possibleCoeffs)-1)]
        
        possibleCoeffs = np.logspace(np.log10(prevCoeff), np.log10(nextCoeff), num=9)
        
    return GetDecisiveFunction(trainingDataset, possibleCoeffs[4])