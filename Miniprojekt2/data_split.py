#
# 
#

import csv
import random

#Splits the scaled data randomly
def GetDataSplit(trainingSize = 2/3, testingSize = 1/3):
    
    probSum = trainingSize + testingSize
    
    trainingSize /= probSum
    testingSize /= probSum
    
    trainingData = []
    testingData = []
    
    with open('data/rp.data', 'r') as data:
        
        reader = csv.reader(data, delimiter='\t')
        
        for row in reader:
            randVal = random.random() # Float from range 0-1
            
            try:
                rowNumbers = row[0].split()
                rowToAppend = [int(i) for i in rowNumbers]
                
                if randVal <= trainingSize:
                    trainingData.append(rowToAppend)
                else:
                    testingData.append(rowToAppend)
            except Exception as e:
                pass
      
      
    random.shuffle(trainingData)
    random.shuffle(testingData)         
    return trainingData, testingData 

#Splits the data, so that the training set has appoximately trainingSize of elements of each class, not fully random
def GetBalancedDataSplit(trainingSize = 2/3, testingSize = 1/3):

    probSum = trainingSize + testingSize

    trainingSize /= probSum
    testingSize /= probSum

    class_2_data = []
    class_4_data = []

    with open('data/rp.data', 'r') as data:
        reader = csv.reader(data, delimiter='\t')
        for row in reader:
            try:
                rowNumbers = row[0].split()
                rowToAppend = [int(i) for i in rowNumbers]
                label = rowToAppend[9]
                if label == 2:
                    class_2_data.append(rowToAppend)
                elif label == 4:
                    class_4_data.append(rowToAppend)
            except Exception as e:
                pass

    trainingData_2 = random.sample(class_2_data, int(len(class_2_data) * trainingSize))
    testingData_2 = [item for item in class_2_data if item not in trainingData_2]

    trainingData_4 = random.sample(class_4_data, int(len(class_4_data) * trainingSize))
    testingData_4 = [item for item in class_4_data if item not in trainingData_4]

    trainingData = trainingData_2 + trainingData_4
    testingData = testingData_2 + testingData_4

    random.shuffle(trainingData)
    random.shuffle(testingData)
    return trainingData, testingData