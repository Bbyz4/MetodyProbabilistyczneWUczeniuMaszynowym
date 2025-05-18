#
#
#

import numpy as np

class KernelFunction():
    
    #Currently supported kernel types: linear, polynomial, rbf
    
    def __init__(self, kernelType = 'linear', degree = 1, gamma = 1.0, coef0 = 0):
        self.kernelType = kernelType
        self.degree = degree
        self.gamma = gamma
        self.coef0 = coef0
        
    def __call__(self, x_1, x_2):
        if self.kernelType == 'linear':
            return self._Linear(x_1, x_2)
        elif self.kernelType == 'poly':
            return self._Polynomial(x_1, x_2, self.degree, self.gamma, self.coef0)
        elif self.kernelType == 'rbf':
            return self._RBF(x_1, x_2, self.gamma)
        else:
            raise ValueError(f"Unknown kernel type: {self.kernelType}")
        
        
    @staticmethod
    def _Linear(x_1, x_2):
        return np.dot(x_1, x_2)
    
    @staticmethod
    def _Polynomial(x_1, x_2, degree, gamma, coef0):
        return (gamma * np.dot(x_1, x_2) + coef0) ** degree
    
    @staticmethod
    def _RBF(x_1, x_2, gamma):
        return np.exp(-gamma * np.linalg.norm(np.array(x_1) - np.array(x_2))**2)