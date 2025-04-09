#
# - Polynominal relation: y = sum(theta_i * x_i^k) for k > 1
#
#
#
import data_split as ds
import numpy as np
import matplotlib.pyplot as plt
import math

NUMBER_OF_TOTAL_TRIES = 1

GRADIENT_DESCENT_RATE = 0.1
GRADIENT_DESCENT_ITERATIONS = 1000
POLYNOMINAL_DEGREE = 1
REGULARIZATION_ITERATIONS = 3

trainingSetSetParts = {
    1: {}
}

checkedParameters = [
    (0.1,1000,2,3),
    (0.1,1000,2,0)
]

avgTheta = {
    i: [] for i in range(7)
}

def ConstructEmptyTheta(deg):
    if deg == 0:
        return 0.0
    
    return [ConstructEmptyTheta(deg-1) for _ in range(7)]

def CreateIterationRange(start, end, deg): #Creates a list of all deg element tuples (x_1, x_2, ..., x_deg), where start <= x_1 <= x_2 <= ... <= x_deg
    if deg == 1:
        return [(i,) for i in range(7)]
    
    prevTupleList = CreateIterationRange(start, end, deg-1)
    return [(i,) + tup for tup in prevTupleList for i in range(tup[0]+1)]

commonIterRanges = {
    i: CreateIterationRange(0,6,i) for i in range(1,4)
}


def SolveForTheta():
    
        
    for i in range(NUMBER_OF_TOTAL_TRIES):
        
        print(f"General iteration {i+1} out of {NUMBER_OF_TOTAL_TRIES}")
        
        #Get the datasets
        trainingSet, validatingSet, testingSet = ds.GetDataSplit(0.7,0.15,0.15)

        X_test, y_test = ds.CreateMatrices(testingSet)
        X_val, y_val = ds.CreateMatrices(validatingSet)

        for gradientParams in checkedParameters:

            GRADIENT_DESCENT_RATE = gradientParams[0]
            GRADIENT_DESCENT_ITERATIONS = gradientParams[1]
            POLYNOMINAL_DEGREE = gradientParams[2]
            REGULARIZATION_ITERATIONS = gradientParams[3]
            
            if POLYNOMINAL_DEGREE not in commonIterRanges:
                iterationRange = CreateIterationRange(0,6,POLYNOMINAL_DEGREE)
            else:
                iterationRange = commonIterRanges[POLYNOMINAL_DEGREE]

            for (partNR, part) in enumerate(trainingSetSetParts.keys()):
                
                print(f"Part iteration {partNR+1} out of {len(trainingSetSetParts.keys())}")

                #Create a subset of the training dataset
                elementNumber = int(len(trainingSet) * part)

                trainingSetSubset = trainingSet[:elementNumber]

                X, y = ds.CreateMatrices(trainingSetSubset)
                theta = {tup: 0.0 for tup in iterationRange}
                
                potentialLambdas = [0,0.00001,0.0001,0.001]
                potentailLambdasResults = {}
                bestLambda = 0.0
                
                #Lambda calc
                GRADIENT_DESCENT_ITERATIONS /= 20
                GRADIENT_DESCENT_ITERATIONS = int(GRADIENT_DESCENT_ITERATIONS)
                
                for ii in range(REGULARIZATION_ITERATIONS):
                    
                    print(f"Regularization iteration {ii+1} out of {REGULARIZATION_ITERATIONS}")
                    
                    for currentLambda in potentialLambdas:
                        
                        #Calculate theta for this lambda  
                        for j in range(GRADIENT_DESCENT_ITERATIONS):
                            
                            #
                            y_pred = []
                            m = len(X)
                            
                            for k in range(m):
                                newYPred = 0
                                for tup in iterationRange:
                                    newYPred += theta[tup] * math.prod([X[k][tupElem] for tupElem in tup])
                                y_pred.append(newYPred)
                                
                            y_diff = [y_pred[k] - y[k] for k in range(len(y))]
                            
                            gradient =  {tup: 0.0 for tup in iterationRange}
                            
                            for tup in iterationRange:
                                #Calculate Grad_a_b
                                for k in range(m):
                                    gradient[tup] += y_diff[k] * math.prod([X[k][tupElem] for tupElem in tup])
                                gradient[tup] *= (2/m)
                                gradient[tup] = float(gradient[tup])
                                
                                #l_2 regularization
                                gradient[tup] += 2*currentLambda*theta[tup]
                                
                                #l_1 regularization
                                #gradient[tup] += currentLambda * np.sign(theta[tup])
                                    
                            theta = {key: value - GRADIENT_DESCENT_RATE * gradient[key] for (key, value) in theta.items()}
                            
                            
                        #Check it's accuracy with the validating set
                        y_val_pred = []
                        m = len(X_val)
                        
                        for k in range(m):
                            newYPred = 0
                            for tup in iterationRange:
                                newYPred += theta[tup] * math.prod([X_val[k][tupElem] for tupElem in tup])
                            y_val_pred.append(newYPred)
                        
                        quadraticError = np.sum((y_val_pred - y_val) ** 2)/len(testingSet)
                        
                        potentailLambdasResults[currentLambda] = quadraticError
                        
                    bestLambda = min(potentailLambdasResults, key=potentailLambdasResults.get)
                    
                    potentailLambdasResults = {float(key): float(value) for (key, value) in potentailLambdasResults.items()}
                    
                    if bestLambda == 0:
                        potentialLambdas = [max(bestLambda + bb, 0.0) for bb in np.arange(bestLambda, bestLambda + (10/pow(10,ii+1)), (1/pow(10,ii+1)))]
                    else:
                        potentialLambdas = [max(bestLambda + bb, 0.0) for bb in np.arange(bestLambda - (4/pow(10,ii+1)), bestLambda + (5/pow(10,ii+1)), (1/pow(10,ii+1)))]
                
                GRADIENT_DESCENT_ITERATIONS *= 20
                
                print(f"Best lambda: {bestLambda}")
                        
                #Train the model using the best computed lambda
                for j in range(GRADIENT_DESCENT_ITERATIONS):
                    
                    #
                    y_pred = []
                    m = len(X)
                    
                    for k in range(m):
                        newYPred = 0
                        for tup in iterationRange:
                            newYPred += theta[tup] * math.prod([X[k][tupElem] for tupElem in tup])
                        y_pred.append(newYPred)
                        
                    y_diff = [y_pred[k] - y[k] for k in range(len(y))]
                    
                    gradient =  {tup: 0.0 for tup in iterationRange}
                    
                    for tup in iterationRange:
                        #Calculate Grad_a_b
                        for k in range(m):
                            gradient[tup] += y_diff[k] * math.prod([X[k][tupElem] for tupElem in tup])
                        gradient[tup] *= (2/m)
                        gradient[tup] = float(gradient[tup])
                        
                        #l_2 regularization
                        gradient[tup] += 2*bestLambda*theta[tup]
                            
                    theta = {key: value - GRADIENT_DESCENT_RATE * gradient[key] for (key, value) in theta.items()}

                #Push to avgTheta
                if part == 1:
                    avgTheta[POLYNOMINAL_DEGREE].append(theta)

                #Calculate the error
                y_pred = []
                m = len(X_test)
                
                for k in range(m):
                    newYPred = 0
                    for tup in iterationRange:
                        newYPred += theta[tup] * math.prod([X_test[k][tupElem] for tupElem in tup])
                    y_pred.append(newYPred)
                
                quadraticError = np.sum((y_pred - y_test) ** 2)/len(testingSet)
                
                if gradientParams not in trainingSetSetParts[part].keys():
                    trainingSetSetParts[part][gradientParams] = []
                
                
                trainingSetSetParts[part][gradientParams].append(float(quadraticError))
           
           
def Plot():
    x_values = list(trainingSetSetParts.keys())
    num_params = len(checkedParameters)
    offset_amount = 0.005 

    plt.figure(figsize=(12, 7))

    for param_index, gradientParams in enumerate(checkedParameters):
        y_values = []
        for part in x_values:
            if gradientParams in trainingSetSetParts[part]:
                y_values.append(np.mean(trainingSetSetParts[part][gradientParams]))
            else:
                y_values.append(np.nan)

        # Apply horizontal offset to x-values
        offset_x_values = [x + (param_index - (num_params - 1) / 2) * offset_amount for x in x_values]

        plt.plot(offset_x_values, y_values, 'o', label=f"Reg {gradientParams[3]}")
        print(y_values)

    plt.xlabel("Fraction of Training Set Used")
    plt.ylabel("Average Quadratic Error on Testing Set")
    plt.title("Comparation between polynominal degrees in models")
    plt.xticks(x_values)  # Keep original x-ticks
    plt.legend()
    plt.show()
     

SolveForTheta()
Plot()

for k in avgTheta.keys():
    if avgTheta[k] != []:
        thetaToPrint = {key: sum(avgTheta[k][i][key] for i in range(len(avgTheta[k])))/len(avgTheta[k]) for key in avgTheta[k][0].keys()}
        print(f"For k = {k}, average theta = {thetaToPrint}")