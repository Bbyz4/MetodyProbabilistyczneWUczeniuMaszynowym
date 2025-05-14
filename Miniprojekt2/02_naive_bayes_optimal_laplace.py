# 02 - Doing some research about the optimal laplace smoothing coefficient

from naive_bayes import GetDecisiveFunction
import data_split as ds
import numpy as np
import matplotlib.pyplot as plt

checkedCoefficients = [coeff for coeff in np.arange(0.000001,0.00001,0.00000001)]
checkedCoefficients.extend([coeff for coeff in np.arange(0.00001,0.0001,0.0000001)])
checkedCoefficients.extend([coeff for coeff in np.arange(0.0001,0.001,0.000001)])
checkedCoefficients.extend([coeff for coeff in np.arange(0.001,0.01,0.00001)]) 
laplaceCoefficientResults = {coeff: [] for coeff in checkedCoefficients}

NUMBER_OF_TOTAL_TRIES = 20

def PerformTests():
    for z in range(NUMBER_OF_TOTAL_TRIES):
        print(f"Try {z+1} in {NUMBER_OF_TOTAL_TRIES}")
        
        trainingSet, testingSet = ds.GetDataSplit()
        
        for coeff in checkedCoefficients:
            decisiveFunction = GetDecisiveFunction(trainingSet, coeff)
            
            totalLoss = 0
            wrongPredictions = 0
            
            for X_test in testingSet:
                predictedClass, probability = decisiveFunction(X_test[0:9])
                
                if(predictedClass == X_test[9]):
                    totalLoss += 1-probability
                else:
                    totalLoss += probability
                    wrongPredictions += 1
                    
            totalLoss/=len(testingSet)
            wrongPredictions/=len(testingSet)
                    
            laplaceCoefficientResults[coeff].append((totalLoss, wrongPredictions))
            
def PlotResults():

    X = list(laplaceCoefficientResults.keys())
    Y_loss = []
    Y_wrong = []
    
    for x in X:
        loss, wrong = zip(*laplaceCoefficientResults[x])
        Y_loss.append(np.mean(loss))
        Y_wrong.append(np.mean(wrong))
        
    print(Y_loss)
    
    plt.figure(figsize=(12,8))
    plt.plot(X, Y_loss, marker='o', linestyle='-', color='b', label='Average Calculated Loss')
    plt.plot(X, Y_wrong, marker='o', linestyle='-', color='r', label='Average Wrong Predictions')
    
    plt.xlabel("Laplace Smoothing Coefficient")
    plt.ylabel("Loss indicators")
    plt.title("Comparasion between different Laplace Smoothing Coefficients")
    
    plt.xscale('log')
    
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    PerformTests()
    PlotResults()