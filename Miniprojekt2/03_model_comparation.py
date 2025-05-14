# 03 - Comparing and plotting the results obtained by using different algorithms

import naive_bayes
import logistic_regression
import data_split as ds

import numpy as np
import matplotlib.pyplot as plt

NUMBER_OF_TOTAL_TRIES = 10
TESTED_TRAINING_SET_PARTS = [0.01,0.02,0.03,0.05,0.08,0.125,0.3,0.625,1]

POSITIVE_CLASS = 4
NEGATIVE_CLASS = 2

#Returns a pair (lossFunctionValue, numberOfWrongPredictions)
def CalculateDecisiveFunctionLoss(testingSet, decisiveFunction):
    totalLoss = 0
    wrongPredictions = 0
    
    accuracy = 0
    
    
    for record in testingSet:
        predictedClass, probability = decisiveFunction(record[0:9])
        
        if predictedClass == record[9]:
            totalLoss += 1-probability
        else:
            totalLoss += probability
            wrongPredictions += 1
            
    totalLoss /= len(testingSet)
    wrongPredictions /= len(testingSet)
    
    return totalLoss, wrongPredictions

#Returns a dictionary that maps training set parts to a list of errors obtained when using that part
def PerformNaiveBayesTests():
    
    results= {part: [] for part in TESTED_TRAINING_SET_PARTS}
    
    for z in range(NUMBER_OF_TOTAL_TRIES):
        print(f"Bayes test {z+1} out of {NUMBER_OF_TOTAL_TRIES}")
        
        trainingSet, testingSet = ds.GetDataSplit()
        
        for part in TESTED_TRAINING_SET_PARTS:
            
            elementNumber = int(len(trainingSet) * part)
            trainingSetPart = trainingSet[:elementNumber]

            try:
                decisiveFunction = naive_bayes.GetDecisiveFunctionWithCrossValidation(trainingSetPart)
                
                totalLoss, wrongPredictions = CalculateDecisiveFunctionLoss(testingSet, decisiveFunction)
                
                results[part].append((totalLoss, wrongPredictions))
            except ValueError:
                print(f"03.PerformNaiveBayesTests: Unlucky training set part for part = {part}")
        
    return results

def PerformLogisticRegressionTests():
    
    results= {part: [] for part in TESTED_TRAINING_SET_PARTS}
    
    for z in range(NUMBER_OF_TOTAL_TRIES):
        print(f"Regression test {z+1} out of {NUMBER_OF_TOTAL_TRIES}")
        
        trainingSet, testingSet = ds.GetDataSplit()
        
        for part in TESTED_TRAINING_SET_PARTS:
            
            elementNumber = int(len(trainingSet) * part)
            trainingSetPart = trainingSet[:elementNumber]
            
            try:
                decisiveFunction = logistic_regression.GetDecisiveFunction(trainingSetPart)
                
                totalLoss, wrongPredictions = CalculateDecisiveFunctionLoss(testingSet, decisiveFunction)
                
                results[part].append((totalLoss, wrongPredictions))
            except ValueError:
                print(f"03.PerformLogisticRegressionTests: Unlucky training set part for part = {part}")
                
    return results

def PerformBothTests():
    
    bayesResults = {part: [] for part in TESTED_TRAINING_SET_PARTS}
    regressionResults = {part: [] for part in TESTED_TRAINING_SET_PARTS}
    
    for z in range(NUMBER_OF_TOTAL_TRIES):
        print(f"Combined test {z+1} out of {NUMBER_OF_TOTAL_TRIES}")
        
        trainingSet, testingSet = ds.GetBalancedDataSplit()
        
        for part in TESTED_TRAINING_SET_PARTS:
            
            elementNumber = int(len(trainingSet) * part)
            trainingSetPart = trainingSet[:elementNumber]
            
            try:
                bayesDecisiveFunction = naive_bayes.GetDecisiveFunctionWithCrossValidation(trainingSetPart)
                
                totalLoss, wrongPredictions = CalculateDecisiveFunctionLoss(testingSet, bayesDecisiveFunction)
                
                bayesResults[part].append((totalLoss, wrongPredictions))
                
                regressionDecisiveFunction = logistic_regression.GetDecisiveFunction(trainingSetPart, 20000, 0.25)
                
                totalLoss, wrongPredictions = CalculateDecisiveFunctionLoss(testingSet, regressionDecisiveFunction)
                
                regressionResults[part].append((totalLoss, wrongPredictions))
            except ValueError:
                print(f"03.PerformBothTests: Unlucky training set part for part = {part}")
                
    return bayesResults, regressionResults

#Assumes result is a dictionary returned by some of the previous methods
def PlotResults(results, title):
    X = list(results.keys())
    #Y = []
    
    Y_loss = []
    Y_wrong = []
    
    for x in X:
        #Y.append(np.mean(results[x]))
        
        x_loss = [item[0] for item in results[x]]
        Y_loss.append(np.mean(x_loss))
        
        x_wrong = [item[1] for item in results[x]]
        Y_wrong.append(np.mean(x_wrong))
        
        
    plt.figure(figsize=(12,8))
    plt.plot(X, Y_loss, marker='x', color='b', linestyle='', label='Average loss function value')
    plt.plot(X, Y_wrong, marker='o', color='b', linestyle='', label='Average wrong predictions')
    
    #plt.errorbar(X, Y, yerr=[[Y[i]-Y_min[i] for i in range(len(X))],[Y_max[i]-Y[i] for i in range(len(X))]],
    #             fmt='none',  
    #             ecolor='b',  
    #             capsize=5,  
    #           label='Average loss range (min to max)')
    
    plt.xlabel("Training set part used")
    plt.ylabel("Loss function value")
    plt.title(title)
    
    plt.xticks(X)
    
    plt.legend()
    plt.tight_layout()
    plt.show()
    
def ComparingPlot(bayesResults, regressionResults):
    X = list(bayesResults.keys())
    #Y = []
    
    Bayes_Y_loss = []
    Bayes_Y_wrong = []
    
    for x in X:
        #Y.append(np.mean(results[x]))
        
        Bayes_x_loss = [item[0] for item in bayesResults[x]]
        Bayes_Y_loss.append(np.mean(Bayes_x_loss))
        
        Bayes_x_wrong = [item[1] for item in bayesResults[x]]
        Bayes_Y_wrong.append(np.mean(Bayes_x_wrong))
        
    
    Regression_Y_loss = []
    Regression_Y_wrong = []

    for x in X:
        #Y.append(np.mean(results[x]))

        Regression_x_loss = [item[0] for item in regressionResults[x]]
        Regression_Y_loss.append(np.mean(Regression_x_loss))

        Regression_x_wrong = [item[1] for item in regressionResults[x]]
        Regression_Y_wrong.append(np.mean(Regression_x_wrong))    
        
    plt.figure(figsize=(12,8))
    
    plt.plot(X, Bayes_Y_loss, marker='x', color='b', linestyle='', label='(Bayes)Average loss function value')
    plt.plot(X, Bayes_Y_wrong, marker='o', color='b', linestyle='', label='(Bayes)Average wrong predictions')
    
    plt.plot(X, Regression_Y_loss, marker='x', color='r', linestyle='', label='(Regression)Average loss function value')
    plt.plot(X, Regression_Y_wrong, marker='o', color='r', linestyle='', label='(Regression)Average wrong predictions')
    
    #plt.errorbar(X, Y, yerr=[[Y[i]-Y_min[i] for i in range(len(X))],[Y_max[i]-Y[i] for i in range(len(X))]],
    #             fmt='none',  
    #             ecolor='b',  
    #             capsize=5,  
    #           label='Average loss range (min to max)')
    
    plt.xlabel("Training set part used")
    plt.ylabel("Loss function value")
    plt.title("Comparation")
    
    plt.xticks(X)
    
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    
if __name__ == "__main__":
    bayesResults, regressionResults = PerformBothTests()
    ComparingPlot(bayesResults,regressionResults)