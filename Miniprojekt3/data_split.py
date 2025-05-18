#
# 
#

import csv
import random

#Splits the scaled data randomly
def GetDataSplit(getScaled = False, trainingSize = 0.7, validatingSize = 0.15, testingSize = 0.15):
    
    probSum = trainingSize + validatingSize + testingSize
    
    trainingSize /= probSum
    validatingSize /= probSum
    testingSize /= probSum
    
    trainingData = []
    validatingData = []
    testingData = []
    
    with open('data/phishing.data' if not getScaled else 'data/phishingScaled.data', 'r', newline='') as data:
        
        reader = csv.reader(data, delimiter=',')
        for row in reader:
            randVal = random.random() # Float from range 0-1
            
            try:
                rowToAppend = [float(i) for i in row]
                
                if randVal <= trainingSize:
                    trainingData.append(rowToAppend)
                elif randVal <= trainingSize + validatingSize:
                    validatingData.append(rowToAppend)
                else:
                    testingData.append(rowToAppend)
            except Exception as e:
                pass
    
    random.shuffle(trainingData)
    random.shuffle(validatingData)
    random.shuffle(testingData)         
    return trainingData, validatingData, testingData 

#Splits the data, so that the training set has appoximately trainingSize of elements of each class, not fully random
def GetBalancedDataSplit(getScaled = False, trainingSize = 0.7, validatingSize = 0.15, testingSize = 0.15):

    probSum = trainingSize + validatingSize + testingSize
    
    trainingSize /= probSum
    validatingSize /= probSum
    testingSize /= probSum

    positive_class_data = []
    negative_class_data = []

    with open('data/phishing.data' if not getScaled else 'data/phishingScaled.data', 'r') as data:
        reader = csv.reader(data, delimiter=',')
        for row in reader:
            try:
                rowNumbers = row[0].split()
                rowToAppend = [int(i) for i in rowNumbers]
                label = rowToAppend[-1]
                if label == 1:
                    positive_class_data.append(rowToAppend)
                elif label == -1:
                    negative_class_data.append(rowToAppend)
            except Exception as e:
                pass

    # Positive class
    training_indices = set(random.sample(range(len(positive_class_data)), int(len(positive_class_data) * trainingSize)))
    trainingData_positive = [positive_class_data[i] for i in training_indices]
    positive_leftovers_indices = [i for i in range(len(positive_class_data)) if i not in training_indices]

    val_ratio = validatingSize / (validatingSize + testingSize)
    val_sample_size = int(len(positive_leftovers_indices) * val_ratio)
    validating_indices = set(random.sample(positive_leftovers_indices, val_sample_size))

    validatingData_positive = [positive_class_data[i] for i in validating_indices]
    testingData_positive = [positive_class_data[i] for i in positive_leftovers_indices if i not in validating_indices]

    # Negative class
    training_indices = set(random.sample(range(len(negative_class_data)), int(len(negative_class_data) * trainingSize)))
    trainingData_negative = [negative_class_data[i] for i in training_indices]
    negative_leftovers_indices = [i for i in range(len(negative_class_data)) if i not in training_indices]

    val_sample_size = int(len(negative_leftovers_indices) * val_ratio)
    validating_indices = set(random.sample(negative_leftovers_indices, val_sample_size))

    validatingData_negative = [negative_class_data[i] for i in validating_indices]
    testingData_negative = [negative_class_data[i] for i in negative_leftovers_indices if i not in validating_indices]

    trainingData = trainingData_positive + trainingData_negative
    validatingData = validatingData_positive + validatingData_negative
    testingData = testingData_positive + testingData_negative

    random.shuffle(trainingData)
    random.shuffle(validatingData)
    random.shuffle(testingData)
    return trainingData, validatingData, testingData