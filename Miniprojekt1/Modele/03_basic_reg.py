#
# - Quadratic loss function
# - No regularization
# - Trivial base functions
# - Solution is calculated using the analytical formula
#
import data_split as ds
import numpy as np
import matplotlib.pyplot as plt

NUMBER_OF_TOTAL_TRIES = 100

GRADIENT_DESCENT_RATE = 0.1
GRADIENT_DESCENT_ITERATIONS = 1000

trainingSetSetParts = {
    1: {}
}

checkedParameters = [
    (0.1,1000),
    (0,0) #special for analytical calculation
]

avgtheta = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]

potentialLambdaValues = np.logspace(-4,3)

def SolveForTheta():
    
    for i in range(NUMBER_OF_TOTAL_TRIES):
        
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

                #Analytical method of solving
                X, y = ds.CreateMatrices(trainingSetSubset)
                theta = [0.0 for _ in range(7)]
                
                if GRADIENT_DESCENT_ITERATIONS != 0:
                    #Gradient method    
                    for j in range(GRADIENT_DESCENT_ITERATIONS):
                        y_pred = X @ theta
                        y_diff = [y_pred[k] - y[k] for k in range(len(y))]
                        gradient = (2 / len(y)) * X.T @ y_diff
                        theta = theta - GRADIENT_DESCENT_RATE * gradient
                else:
                    #Analytical method
                    theta = np.linalg.inv(X.T @ X) @ (X.T @ y)
                    

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

        plt.plot(offset_x_values, y_values, 'o', label=(f"Rate={gradientParams[0]}, Iter={gradientParams[1]}" if gradientParams[1] != 0 else "Analytical method"))

    plt.xlabel("Fraction of Training Set Used")
    plt.ylabel("Average Quadratic Error on Testing Set")
    plt.title("Error vs. Training Set Size for Different Gradient Parameters")
    plt.xticks(x_values)  # Keep original x-ticks
    plt.legend()
    plt.show()
    
def PlotLambdas():
    x_values = list(lambdaResults.keys())
    y_values = [np.mean(value) for value in lambdaResults.values()]
    
    plt.xlabel("")
     

SolveForTheta()
Plot()