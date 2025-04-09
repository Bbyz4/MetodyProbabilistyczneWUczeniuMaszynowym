#
# - Quadratic loss function
# - No regularization
# - Trivial base functions
# - Solution is calculated using the analytical formula
#
import data_split as ds
import numpy as np
import matplotlib.pyplot as plt
import time
import random

NUMBER_OF_TOTAL_TRIES = 50

trainingSetSetParts = {
    1: {}
}

checkedParameters = [
    (0.1,10,2),
    (0.1,100,2),
    (0.1,1000,2),
    (0.1,100,0),
    (0.1,1000,0),
    (0,0,0) #special for analytical calculation
]

gradientMethodNames = {
    0: "BGD",
    1: "SGD",
    2: "Mini-batch(10%)",
}     

gradientCalcTimes = {
    0: [],
    1: [],
    2: []
}

avgtheta = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]

def SolveForTheta():
    
        
    for i in range(NUMBER_OF_TOTAL_TRIES):
        
        print(f"Try {i+1} out of {NUMBER_OF_TOTAL_TRIES}")
        
        #Get the datasets
        trainingSet, validatingSet, testingSet = ds.GetDataSplit(0.85,0,0.15)

        X_test, y_test = ds.CreateMatrices(testingSet)

        for gradientParams in checkedParameters:

            GRADIENT_DESCENT_RATE = gradientParams[0]
            GRADIENT_DESCENT_ITERATIONS = gradientParams[1]
            GRADIENT_TYPE = gradientParams[2]

            for part in trainingSetSetParts.keys():

                #Create a subset of the training dataset
                elementNumber = int(len(trainingSet) * part)

                trainingSetSubset = trainingSet[:elementNumber]

                #Analytical method of solving
                X, y = ds.CreateMatrices(trainingSetSubset)
                theta = [0.0 for _ in range(7)]
                
                gradient_start_time = time.perf_counter()
                
                if GRADIENT_DESCENT_ITERATIONS != 0:
                    # Gradient method
                    if GRADIENT_TYPE == 0:  # BGD
                        for j in range(GRADIENT_DESCENT_ITERATIONS):
                            y_pred = X @ theta
                            y_diff = [y_pred[k] - y[k] for k in range(len(y))]
                            gradient = (2 / len(y)) * X.T @ y_diff
                            theta = theta - GRADIENT_DESCENT_RATE * gradient
                    elif GRADIENT_TYPE == 1:  # SGD
                        for j in range(GRADIENT_DESCENT_ITERATIONS):
                            randomOrder = [l for l in range(len(y))]
                            random.shuffle(randomOrder)
                            for k in randomOrder:
                                x_single = X[k:k + 1]
                                y_single = y[k:k + 1]
                                y_pred_single = x_single @ theta
                                y_diff_single = y_pred_single - y_single
                                gradient = 2 * x_single.T @ y_diff_single
                                theta = theta - GRADIENT_DESCENT_RATE * gradient.flatten()
                    elif GRADIENT_TYPE == 2:  # Minibatch (10% subset)
                        batch_size = int(len(y) * 0.1)
                        if batch_size < 1:
                            batch_size = 1

                        for j in range(GRADIENT_DESCENT_ITERATIONS):
                            
                            random.shuffle(trainingSetSubset)
                            X, y = ds.CreateMatrices(trainingSetSubset)
                            
                            for k in range(0,len(y),batch_size):
                                X_batch = X[k:k + batch_size]
                                y_batch = y[k:k + batch_size]
                                y_pred = X_batch @ theta
                                y_diff = [y_pred[l] - y_batch[l] for l in range(len(y_batch))]
                                gradient = (2 / len(y_batch)) * X_batch.T @ y_diff
                                theta = theta - GRADIENT_DESCENT_RATE * gradient
                else:
                    #Analytical method
                    theta = np.linalg.inv(X.T @ X) @ (X.T @ y)
                    
                gradient_end_time = time.perf_counter()
                gradient_time_taken = gradient_end_time - gradient_start_time
                
                if GRADIENT_DESCENT_ITERATIONS != 0:
                    gradientCalcTimes[GRADIENT_TYPE].append(gradient_time_taken)
                    
                #Calculate the error
                y_pred = X_test @ theta
                
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

        plt.plot(offset_x_values, y_values, 'o', label=(f"({gradientMethodNames[gradientParams[2]]},{gradientParams[0]},{gradientParams[1]})" if gradientParams[1] != 0 else "Analytical method"))

    plt.xlabel("Fraction of Training Set Used")
    plt.ylabel("Average Quadratic Error on Testing Set")
    plt.title("Error vs. Training Set Size for Different Gradient Parameters")
    plt.xticks(x_values)  # Keep original x-ticks
    plt.legend()
    plt.show()
     

SolveForTheta()
Plot()

#for (key, value) in gradientCalcTimes.items():
#    print(f"Average time for {gradientMethodNames[key]} was {np.mean(value)}")