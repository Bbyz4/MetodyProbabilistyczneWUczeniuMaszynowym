#
# 
#

import csv
import random
import numpy as np

#Splits the scaled data randomly
def GetDataSplit(trainingSize = 0.7, validatingSize = 0.15, testingSize = 0.15):
    
    probSum = trainingSize + validatingSize + testingSize
    
    trainingSize /= probSum
    validatingSize /= probSum
    testingSize /= probSum
    
    trainingData = []
    validatingData = []
    testingData = []
    
    with open('../data/daneScaled.data', 'r') as data:
        
        reader = csv.reader(data, delimiter='\t')
        
        for row in reader:
            randVal = random.random() # Float from range 0-1
            
            row = [float(i) for i in row]
            
            if randVal <= trainingSize:
                trainingData.append(row)
            elif randVal <= trainingSize + validatingSize:
                validatingData.append(row)
            else:
                testingData.append(row)
      
      
    random.shuffle(trainingData)
    random.shuffle(validatingData)
    random.shuffle(testingData)         
    return trainingData, validatingData, testingData     

#Data is a list of tuples, where the last value is y
def CreateMatrices(data):
    data = np.array(data)
    X = data[:, :-1]
    y = data[:, -1]
    if X.shape[0] != y.shape[0] or X.shape[1]!=7:
        print("Error: data_split: CreateMatrices: wrong dimensions!")
    return X, y