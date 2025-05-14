# 04 - Comparing different gradient parameters when using the logistic regression method

import logistic_regression
import data_split as ds

import numpy as np
import matplotlib.pyplot as plt

NUMBER_OF_TOTAL_TRIES = 20

def PerformTests():
    
    results = {a : [] for a in np.arange(5000, 51000, 1000)}
    
    for z in range(NUMBER_OF_TOTAL_TRIES):
        print(f"Regression test {z+1} out of {NUMBER_OF_TOTAL_TRIES}")
        
        trainingSet, testingSet = ds.GetBalancedDataSplit()
        
        decisiveFunctionList = logistic_regression.GetLossFunctionValuesForComparation(trainingSet, 50000, 1000, 0.5)
        
        for k in range(len(decisiveFunctionList)):
            results[(k+1)*1000 + 4000].append(decisiveFunctionList[k])
                
    return results

def PlotResults(results):

    X = list(results.keys())
    Y = []
    
    X_labels = [str(x) for x in X]
    
    for x in X:
        Y.append(np.mean(results[x]))
    
    plt.figure(figsize=(12,8))
    plt.plot(X_labels, Y, marker='o', linestyle='', color='b', label='Average Calculated Loss')
    
    plt.xlabel("Number of gradient descent iterations")
    plt.ylabel("Calculated loss function (J)")
    plt.title("Logistic regression gradient descent iterations parameter comparation")
    
    plt.xticks(X_labels, rotation=45, ha='right')
    
    plt.legend()
    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    results = PerformTests()
    PlotResults(results)