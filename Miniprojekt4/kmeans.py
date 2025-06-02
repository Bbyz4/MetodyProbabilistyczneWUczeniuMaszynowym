import numpy as np
import random
import data_load as dl
import math
import coolplots
import matplotlib.pyplot as plt

import utils

def KmeansClassifyPoints(originalPoints, points, k, isVisualized, isPlusPlus, dataID=0):

    if(len(points) < k):
        raise ValueError("KmeansClassifyPoints: Invalid k")    
    
    centroids = []
    
    if not isPlusPlus:
        centroids = random.sample(points, k)
    else:
        centroids.append(random.choice(points))

        for _ in range(1, k):
            distances = []

            for p in points:
                min_dist_sq = min(utils.EuclideanDistSquared(p,c) for c in centroids)
                distances.append(min_dist_sq)

            total = sum(distances)
            probs = [d / total for d in distances]
            cumulative_probs = np.cumsum(probs)

            r = random.random()
            for i, cp in enumerate(cumulative_probs):
                if r < cp:
                    centroids.append(points[i])
                    break
        
    pointsClusters = [0] * len(points)
    
    pointChangedClasses = True
    
    pointKeyFrames = []
    centroidKeyFrames = []
    
    while(pointChangedClasses):
        pointChangedClasses = False
        
        #Classify points
        #If anything changed in their classification, the loop should continue
        for i, point in enumerate(points):
            currentMinDist = math.inf
            currentClosestCentroid = -1
            
            for j, centroid in enumerate(centroids):
                dist = math.sqrt(utils.EuclideanDistSquared(point, centroid))
                
                if(dist < currentMinDist):
                    currentMinDist = dist
                    currentClosestCentroid = j
    
            if(pointsClusters[i] != currentClosestCentroid):
                pointChangedClasses = True
            pointsClusters[i] = currentClosestCentroid
            
        if isVisualized:
            pointKeyFrames.append(list(pointsClusters))
            centroidKeyFrames.append(list(centroids))
    
        #Change centroids
        for cluster in range(k):
            pointsInOurCluster = [p for i, p in enumerate(points) if pointsClusters[i]==cluster]
            
            if pointsInOurCluster:
                newCentroid = np.mean(pointsInOurCluster, axis=0)
            else:
                newCentroid = random.choice(points) #Random reinicialization
                
            centroids[cluster] = newCentroid
        
        
    if isVisualized:
        diff = False
        
        for i in range(len(points)):
            if points[i] != originalPoints[i]:
                diff = True
                break
                
        if diff:
            coolplots.PlotKmeansIterationsAfterMapping(originalPoints, points, pointKeyFrames, centroidKeyFrames, framesPerTransition=60, dataID=dataID)
        else:
            coolplots.PlotKmeansIterations(points, pointKeyFrames, centroidKeyFrames, framesPerTransition=60, dataID=dataID)
        
    MSE = 0
    
    for i in range(len(points)):
        MSE += utils.EuclideanDistSquared(points[i], centroids[pointsClusters[i]])
        
    return MSE

def KMeansElbowMethod(points, tryNumberPerK):
    
    testedK = [k for k in range(3,36)]
    calculatedErrorsNoPlus = []
    calculatedErrorsWithPlus = []
    
    for k in testedK:
        print(f"KMeansElbowMethod: testing k = {k}")
        
        totalMSENoPlus = 0
        totalMSEWithPlus = 0
        
        for _ in range(tryNumberPerK):
            totalMSENoPlus += KmeansClassifyPoints(points, points, k, isVisualized=False, isPlusPlus=False)
            totalMSEWithPlus += KmeansClassifyPoints(points, points, k, isVisualized=False, isPlusPlus=True)
            
        calculatedErrorsNoPlus.append(totalMSENoPlus/tryNumberPerK)
        calculatedErrorsWithPlus.append(totalMSEWithPlus/tryNumberPerK)
        
    plt.figure(figsize=(12,12))
    
    plt.xlabel("K value")
    plt.ylabel("MSE score")
    plt.title("Elbow method for KMeans algorithm")
    
    plt.plot(testedK, calculatedErrorsNoPlus, marker='o', color='red', label='Classic', linestyle='')
    plt.plot(testedK, calculatedErrorsWithPlus, marker='o', color='blue', label='Plus Plus', linestyle='')
    
    plt.legend()
    plt.show()