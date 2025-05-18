import data_split as ds
import numpy as np
import matplotlib.pyplot as plt

import svm
import kernel_function as kF

import knn
import distance_function as dF

import ada

#---------------------------------------------SVM----------------------------------------------------

def PerformSVMTests(testNumber, kernelFunctionList):
    results = {kf: [] for kf in kernelFunctionList}
    
    for zz in range(testNumber):
        print(f"SVMTests: test {zz+1} in {testNumber}")
        
        trainingDataset, validatingDataset, testingDataset = ds.GetDataSplit(getScaled=False)
        
        print(f"TRAIN LEN: {len(trainingDataset)}")
        
        for yy, kernelFunction in enumerate(kernelFunctionList):
            print(f"KERNEL {yy+1} out of {len(kernelFunctionList)}")
        
            decFunc = svm.GetDecisiveFunctionUsingSKLearn(trainingDataset, kernelFunction, 0.1)
            accuracy = svm.CalcAccuracy(testingDataset, decFunc)
        
            results[kernelFunction].append(accuracy)
        
    return results

def SVMKernelTests(testNumber = 10):
    
    gammas = np.arange(0.01,0.11,0.01)
    
    #linear_kernel_func = kF.KernelFunction(kernelType='linear')
    polynomial_kernel_funcs = [kF.KernelFunction(kernelType='poly', degree=5, gamma=g, coef0=0) for g in gammas]
    #rbf_kernel_func = kF.KernelFunction(kernelType='rbf', gamma=0.1)
    
    testResult = PerformSVMTests(testNumber, polynomial_kernel_funcs)
    
    kernel_names = [f'Poly 5 with gamma {g}' for g in gammas]
      
    # Plot results  
    plt.figure(figsize=(10, 6))
    plt.boxplot(list(testResult.values()), labels=kernel_names)
    plt.title('SVM Kernel functions comparation')
    plt.xlabel('Kernel Function')
    plt.ylabel('Test Set Accuracy')
    plt.grid(False)
    plt.show()
     
#---------------------------------------------KNN----------------------------------------------------

def PerformKNNTests(testNumber, distanceFunctions):
    results = {df: [] for df in distanceFunctions}
    
    for zz in range(testNumber):
        print(f"KNNTests: test {zz+1} in {testNumber}")
        
        trainingDataset, validatingDataset, testingDataset = ds.GetDataSplit(getScaled=True)
        
        print(f"TRAIN LEN: {len(trainingDataset)}")
        
        for yy, distanceFunction in enumerate(distanceFunctions):
            print(f"DISTANCE FUNCTION {yy+1} out of {len(distanceFunctions)}")
            decFunc = knn.GetDecisiveFunctionWithValidation(trainingDataset, validatingDataset, distanceFunction)
            accuracy = knn.CalcAccuracy(testingDataset, decFunc)
        
            results[distanceFunction].append(accuracy)

    return results

def KNNDistFuncTests(testNumber = 10):
    
    eucidean_dist = dF.MinkowskiDistanceFunction(2)
    manhattan_dist = dF.MinkowskiDistanceFunction(1)
    
    distFuncs = [eucidean_dist, manhattan_dist]
    
    distFunc_names = ['Euclidean', 'Manhattan']
    
    testResult = PerformKNNTests(testNumber, distFuncs)
        
        # Plot results  
    plt.figure(figsize=(10, 6))
    plt.boxplot(list(testResult.values()), labels=distFunc_names)
    plt.title('KNN Distance functions comparation')
    plt.xlabel('Distance Function')
    plt.ylabel('Test Set Accuracy')
    plt.grid(False)
    plt.show()

#---------------------------------------------ADA----------------------------------------------------

def PerformADATests(testNumber, estimatorNumer):
    results = []
    
    for zz in range(testNumber):
        print(f"ADATests: test {zz+1} in {testNumber}")
        
        trainingDataset, validatingDataset, testingDataset = ds.GetDataSplit(getScaled=False)
        
        print(f"TRAIN LEN: {len(trainingDataset)}")
        
        decFunc = ada.GetDecisiveFunction(trainingDataset, estimatorNumer)
        accuracy = ada.CalcAccuracy(testingDataset, decFunc)
        
        results.append(accuracy)

    return results

def ADATests(testNumber = 10):
    
    estimatorNumbers = [100, 500]
    
    results = []
    
    for zz, estNumber in enumerate(estimatorNumbers):
        print(f"DistFunc {zz+1} in {len(estimatorNumbers)}")
        testResult = PerformADATests(testNumber, estNumber)
        results.append(testResult)
        
        # Plot results  
    plt.figure(figsize=(10, 6))
    plt.boxplot(results, labels=estimatorNumbers)
    plt.title('AdaBoost weak estimator number comparation')
    plt.xlabel('Number of weak estimators')
    plt.ylabel('Test Set Accuracy')
    plt.grid(False)
    plt.show()

#---------------------------------------------MAIN---------------------------------------------------    

#SVMKernelTests(50)
#KNNDistFuncTests(10)
ADATests(10)