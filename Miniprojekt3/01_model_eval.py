import data_split as ds
import numpy as np
import matplotlib.pyplot as plt

import svm
import kernel_function as kF

import knn
import distance_function as dF

import ada

import math

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
    
    gammas = [0.1]
    degrees = [5]
    betas = [0]
    
    #linear_kernel_func = kF.KernelFunction(kernelType='linear')
    polynomial_kernel_funcs = [kF.KernelFunction(kernelType='poly', degree=d, gamma=g, coef0=b) for g in gammas for d in degrees for b in betas]
    rbf_kernel_funcs = [kF.KernelFunction(kernelType='rbf', gamma=g) for g in gammas]
    
    testResult = PerformSVMTests(testNumber, polynomial_kernel_funcs)
    
    kernel_names = [f'Best SVM model' for b in betas]
      
    # Plot results  
    plt.figure(figsize=(10, 6))
    plt.boxplot(list(testResult.values()), labels=kernel_names)
    plt.title('RBF Gamma Comparation')
    plt.xlabel('Gamma Value')
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
    
    distFuncs = [dF.MinkowskiDistanceFunction(i) for i in range(1,11)]
    
    #distFuncs = [eucidean_dist, manhattan_dist]
    
    distFunc_names = [f'{i}' for i in range(1,11)]
    
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

def PerformADATests(testNumber, estimatorNumbers):
    results = {est: [] for est in estimatorNumbers}
    
    for zz in range(testNumber):
        print(f"ADATests: test {zz+1} in {testNumber}")
        
        trainingDataset, validatingDataset, testingDataset = ds.GetDataSplit(getScaled=False)
        
        print(f"TRAIN LEN: {len(trainingDataset)}")
        
        for yy, estimator in enumerate(estimatorNumbers):
            print(f"ESTIMATOR {yy+1} in {len(estimatorNumbers)}")
            decFunc = ada.GetDecisiveFunction(trainingDataset, estimator)
            accuracy = ada.CalcAccuracy(testingDataset, decFunc)
            
            results[estimator].append(accuracy)

    return results

def ADATests(testNumber = 10):
    
    estimatorNumbers = [50, 100, 200]
    
    results = []
    testResult = PerformADATests(testNumber, estimatorNumbers)
    
        
        # Plot results  
    plt.figure(figsize=(10, 6))
    plt.boxplot(list(testResult.values()), labels=estimatorNumbers)
    plt.title('AdaBoost weak estimator number comparation')
    plt.xlabel('Number of weak estimators')
    plt.ylabel('Test Set Accuracy')
    plt.grid(False)
    plt.show()

#---------------------------------------------MAIN---------------------------------------------------    

#SVMKernelTests(100)
#KNNDistFuncTests(100)
#ADATests(100)