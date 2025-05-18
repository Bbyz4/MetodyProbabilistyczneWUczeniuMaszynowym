#
#
#

import numpy as np

class MinkowskiDistanceFunction():
    
    def __init__(self, p):
        self.p = p
        
    #Assuming X is a list of vectors and Y is only one vector, returns a list of distances for performance enhancement reasons
    def __call__(self, X, Y):
        X_np = np.array(X)
        Y_np = np.array(Y)
        
        distances = np.power(np.sum(np.power(np.abs(X_np - Y_np), self.p), axis=1), 1/self.p)
        return distances.tolist()
    
