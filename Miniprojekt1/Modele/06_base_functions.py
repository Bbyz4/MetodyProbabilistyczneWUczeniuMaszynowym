#
# - Polynominal relation: y = sum(theta_i * x_i^k) for k > 1
#
#
#
import data_split as ds
import numpy as np
import matplotlib.pyplot as plt

NUMBER_OF_TOTAL_TRIES = 30

GRADIENT_DESCENT_RATE = 0.1
GRADIENT_DESCENT_ITERATIONS = 1000

trainingSetSetParts = {
    0.01: {},
    0.02: {},
    0.05: {},
    0.08: {},
    0.125: {},
    0.3: {},
    0.625: {},
    1: {}
}

checkedParameters = [
    (0.1,1000,round(float(i),2)) for i in np.arange(1.125,1.3,0.025)
    #(0,0,0) #special for analytical calculation
]

avgtheta = {
    i: [] for i in [checkedParameters[j][2] for j in range(len(checkedParameters))]
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

            for part in trainingSetSetParts.keys():

                #Create a subset of the training dataset
                elementNumber = int(len(trainingSet) * part)

                trainingSetSubset = trainingSet[:elementNumber]

                X, y = ds.CreateMatrices(trainingSetSubset)
                theta = [0.0 for _ in range(7)]
                X_pow = [[pow(i,gradientParams[2]) for i in X[j]] for j in range(len(X))]
                X_pow = np.array(X_pow)
                
                if GRADIENT_DESCENT_ITERATIONS != 0:
                    #Gradient method    
                    for j in range(GRADIENT_DESCENT_ITERATIONS):
                        
                        #Modified gradient function
                        y_pred = X_pow @ theta
                        y_diff = [y_pred[k] - y[k] for k in range(len(y))]
                        gradient = (2 / len(y)) * X_pow.T @ y_diff
                        theta = theta - GRADIENT_DESCENT_RATE * gradient
                else:
                    #Analytical method
                    theta = np.linalg.inv(X.T @ X) @ (X.T @ y)
                    

                #Add to avgTheta if the training set size is 100%
                if part == 1:
                    avgtheta[gradientParams[2]].append(theta)

                #Calculate the error
                y_pred = X_test @ theta
                
                if GRADIENT_DESCENT_ITERATIONS != 0:
                    X_test_pow = [[pow(i, gradientParams[2]) for i in X_test[j]] for j in range(len(X_test))]
                    X_test_pow = np.array(X_test_pow)
                    y_pred = X_test_pow @ theta
                
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

        plt.plot(offset_x_values, y_values, 'o', label=f"x^{gradientParams[2]}")

    plt.xlabel("Fraction of Training Set Used")
    plt.ylabel("Average Quadratic Error on Testing Set")
    plt.title("Comparation between polynominal relation models")
    plt.xticks(x_values)  # Keep original x-ticks
    plt.legend()
    plt.show()
     

SolveForTheta()
Plot()

for (key,value) in avgtheta.items():
    print(f"Average theta for x^{key} = {np.mean(value, axis=0)}")