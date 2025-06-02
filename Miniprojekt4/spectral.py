import numpy as np
import random
import data_load as dl
import math
import coolplots
import matplotlib.pyplot as plt
import math

import utils

from enum import Enum

class MatrixConstructMethod(Enum):
    FULL_RBF = 1
    E_DISTANCE = 2
    KNN = 3 #OR method of forcing symmetry

def ConstructAdjacencyMatrix(points, matrixConstructMethod, parameter):
    
    #parameter is:
    #   gamma for RBF
    #   epsilon for E_DIST
    #   k for KNN
    
    n = len(points)
    A = np.zeros((n,n))
    
    match matrixConstructMethod:
        case MatrixConstructMethod.FULL_RBF:
            for i in range(n):
                for j in range(n):
                    A[i][j] = math.exp(-parameter * utils.EuclideanDistSquared(points[i], points[j]))  
                    
        case MatrixConstructMethod.E_DISTANCE:
            for i in range(n):
                for j in range(n):
                    A[i][j] = 1 if utils.EuclideanDistSquared(points[i], points[j]) <= parameter else 0
                    
        case MatrixConstructMethod.KNN:
            for i in range(n):
                closestPointsIndeces = np.argsort([utils.EuclideanDistSquared(points[i], points[j]) for j in range(n)])
                for j in range(1, parameter+1): #we skip i itself which is the closest
                    A[i][closestPointsIndeces[j]] = 1
                    
        case _:
            raise ValueError("ConstructAdjacencyMatrix: invalid construct method!")
    
    return A

def SpectralTransformation(points, desiredDimension, normalizedLaplacian):
    
    n = len(points)
    
    A = ConstructAdjacencyMatrix(points, MatrixConstructMethod.FULL_RBF, 0.1)
    D = np.zeros((n,n))
    
    for i in range(n):
        D[i][i] = sum(A[i][j] for j in range(n))
        
    D_inv_sqrt = np.diag(1.0 / np.sqrt(np.diag(D)))
     
     
       
    if normalizedLaplacian: 
        L = D_inv_sqrt @ (D-A) @ D_inv_sqrt
    else:
        L = D-A
    
    eigenvals, eigenvecs = np.linalg.eigh(L)
    # first eigenval is always 0 with a constant eigenvec    

    eigenvecsForTransformation = eigenvecs[:, 1 : desiredDimension + 1]
    
    result = []
    
    result = [list(eigenvecsForTransformation[i, :]) for i in range(n)]

    resultFloat = [[float(val) for val in row] for row in result]

    return resultFloat