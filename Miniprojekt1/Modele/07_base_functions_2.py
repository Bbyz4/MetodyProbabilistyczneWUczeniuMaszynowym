#
# - Polynominal relation: y = sum(theta_i * x_i^k) for k > 1
#
#
#
import data_split as ds
import numpy as np
import matplotlib.pyplot as plt
import math

NUMBER_OF_TOTAL_TRIES = 50

GRADIENT_DESCENT_RATE = 0.1
GRADIENT_DESCENT_ITERATIONS = 1000
POLYNOMINAL_DEGREE = 2

trainingSetSetParts = {
    1: {}
}

checkedParameters = [
    (0.1,1000,1)
    #(0,0) #special for analytical calculation
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
        
        print(f"Iteration {i+1} out of {NUMBER_OF_TOTAL_TRIES}")
        
        #Get the datasets
        trainingSet, validatingSet, testingSet = ds.GetDataSplit(0.85,0,0.15)

        X_test, y_test = ds.CreateMatrices(testingSet)

        for gradientParams in checkedParameters:

            GRADIENT_DESCENT_RATE = gradientParams[0]
            GRADIENT_DESCENT_ITERATIONS = gradientParams[1]
            POLYNOMINAL_DEGREE = gradientParams[2]
            
            if POLYNOMINAL_DEGREE not in commonIterRanges:
                iterationRange = CreateIterationRange(0,6,POLYNOMINAL_DEGREE)
            else:
                iterationRange = commonIterRanges[POLYNOMINAL_DEGREE]

            for part in trainingSetSetParts.keys():

                #Create a subset of the training dataset
                elementNumber = int(len(trainingSet) * part)

                trainingSetSubset = trainingSet[:elementNumber]

                X, y = ds.CreateMatrices(trainingSetSubset)
                theta = {tup: 0.0 for tup in iterationRange}
                
                if GRADIENT_DESCENT_ITERATIONS != 0:
                    #Gradient method    
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
                              
                        theta = {key: value - GRADIENT_DESCENT_RATE * gradient[key] for (key, value) in theta.items()}
                        
                else:
                    #Analytical method
                    theta = np.linalg.inv(X.T @ X) @ (X.T @ y)


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

        plt.plot(offset_x_values, y_values, 'o', label=f"Feature combinations {gradientParams[2]}")
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