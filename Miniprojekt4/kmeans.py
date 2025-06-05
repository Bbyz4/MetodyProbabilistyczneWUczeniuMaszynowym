import numpy as np
import random
import data_load as dl
import math
import coolplots
import matplotlib.pyplot as plt

import utils

#
# KMEANS CLUSTERIZATION
# RETURNS POINT CLUSTER ASSIGNMENT AND CENTROIDS
#

def KmeansClassifyPoints(originalPoints, points, k, isVisualized, isPlusPlus, dataID=0):

    if(len(points) < k):
        raise ValueError("KmeansClassifyPoints: Invalid k")    
    
    centroids = []
    
    if not isPlusPlus:
        #k-means
        centroids = random.sample(points, k)
    else:
        #k-means++
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
        
    return pointsClusters, centroids

def KMeansElbowMethod(points, tryNumberPerK):
    
    testedK = [k for k in range(2,int(math.sqrt(len(points))))]
    calculatedErrorsNoPlus = []
    calculatedErrorsWithPlus = []
    
    for k in testedK:
        print(f"KMeansElbowMethod: testing k = {k}")
        
        totalMSENoPlus = 0
        totalMSEWithPlus = 0
        
        for _ in range(tryNumberPerK):
            pointsClusters, centroids = KmeansClassifyPoints(points, points, k, isVisualized=False, isPlusPlus=False)
            
            totalMSENoPlus += sum(utils.EuclideanDistSquared(points[i], centroids[pointsClusters[i]]) for i in range(len(points)))
            
            pointsClusters, centroids = KmeansClassifyPoints(points, points, k, isVisualized=False, isPlusPlus=True)
            
            totalMSEWithPlus += sum(utils.EuclideanDistSquared(points[i], centroids[pointsClusters[i]]) for i in range(len(points)))
            
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
    
def KMeansSilhouetteMethod(points, tryNumberPerK):
    
    testedK = [k for k in range(2,int(math.sqrt(len(points))))]
    calculatedSsNoPlus = []
    calculatedSWithPlus = []
    
    for k in testedK:
        print(f"KMeansSilhouetteMethod: testing k = {k}")
        
        SNoPlus = 0
        SWithPlus = 0
        
        for _ in range(tryNumberPerK):
            pointsClusters, centroids = KmeansClassifyPoints(points, points, k, isVisualized=False, isPlusPlus=False)
            
            a = [utils.EuclideanDistSquared(points[i], centroids[pointsClusters[i]]) for i in range(len(points))]
            
            b = [min(utils.EuclideanDistSquared(points[i], centroids[j]) for j in range(len(centroids)) if j!=pointsClusters[i]) for i in range(len(points))]
            
            SNoPlus += (1/len(points))*sum((b[i]-a[i])/(max(b[i], a[i])) for i in range(len(points)))
            
            pointsClusters, centroids = KmeansClassifyPoints(points, points, k, isVisualized=False, isPlusPlus=True)
            
            a = [utils.EuclideanDistSquared(points[i], centroids[pointsClusters[i]]) for i in range(len(points))]
            b = [min(utils.EuclideanDistSquared(points[i], centroids[j]) for j in range(len(centroids)) if j!=pointsClusters[i]) for i in range(len(points))]
            
            SWithPlus += (1/len(points))*sum((b[i]-a[i])/(max(b[i], a[i])) for i in range(len(points)))
            
        calculatedSsNoPlus.append(SNoPlus/tryNumberPerK)
        calculatedSWithPlus.append(SWithPlus/tryNumberPerK)
        
        
    plt.figure(figsize=(12,12))
    
    plt.xlabel("K value")
    plt.ylabel("Silhouette score")
    plt.title("Silhouette method for KMeans algorithm")
    
    plt.plot(testedK, calculatedSsNoPlus, marker='o', color='red', label='Classic', linestyle='')
    plt.plot(testedK, calculatedSWithPlus, marker='o', color='blue', label='Plus Plus', linestyle='')
    
    plt.legend()
    plt.show()