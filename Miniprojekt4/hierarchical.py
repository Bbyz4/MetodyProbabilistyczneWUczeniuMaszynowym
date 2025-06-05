import numpy as np
import random
import data_load as dl
import math
import coolplots
import matplotlib.pyplot as plt
import heapq

import utils

from dsu import DSU

def WardDistance(center1, center2, size1, size2):
    return ((size1*size2/(size1 + size2)) * utils.EuclideanDistSquared(center1, center2))

def HierarchicalClassifyPoints(originalPoints, points, isVisualized, dataID=0):
    
    isAlreadyConnected = [False for _ in range(len(points))]
    
    clusterCenters = [point for point in points]
    clusterSizes = [1 for _ in range(len(points))]
    
    connectionHistory = []
    
    H = []
    
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            heapq.heappush(H, (WardDistance(clusterCenters[i], clusterCenters[j], 1, 1), (i,j)))
        
    currentNewClusterID = len(points)
    currentIteration = 0
        
    while H:
        (D, (i, j)) = heapq.heappop(H)
        
        if not isAlreadyConnected[i] and not isAlreadyConnected[j]:
            #Connect 2 clusters together
            isAlreadyConnected[i] = True
            isAlreadyConnected[j] = True
            
            isAlreadyConnected.append(False)
            clusterCenters.append(list((np.array(clusterCenters[i]) * clusterSizes[i] + np.array(clusterCenters[j]) * clusterSizes[j])/(clusterSizes[i] + clusterSizes[j])))
            clusterSizes.append(clusterSizes[i] + clusterSizes[j])
            
            connectionHistory.append(((i,j), currentIteration, D))
            
            for k in range(currentNewClusterID):
                if not isAlreadyConnected[k]:
                    heapq.heappush(H, (WardDistance(clusterCenters[k], clusterCenters[currentNewClusterID], clusterSizes[k], clusterSizes[currentNewClusterID]), (k, currentNewClusterID)))
                    
            currentNewClusterID += 1
            
        currentIteration += 1

    if isVisualized:
        diff = False
        
        for i in range(len(points)):
            if points[i] != originalPoints[i]:
                diff = True
                break
                
        if diff:
            coolplots.PlotHierarchicalHistoryAfterMapping(originalPoints, points, connectionHistory, dataID)
        else:
            coolplots.PlotHierarchicalHistory(points, connectionHistory, dataID)
        
    return connectionHistory

def GetClusterizationFromHistory(connectionHistory, desiredClusterNumber):
    n = len(connectionHistory) + 1 #number of points
    
    D = DSU(2*n)
    
    for i in range(n - desiredClusterNumber):
        D.union(connectionHistory[i][0][0], connectionHistory[i][0][1])
        D.union(connectionHistory[i][0][0], i+n)
        
    return [D.find(i) for i in range(n)]
    

def HierarchicalDistancePlot(points):
    
    connectionHistory = HierarchicalClassifyPoints(points, points, isVisualized=False)
    
    X = [x for x in range(int(math.sqrt(len(points)))+1, 1, -1)]
    Y = [con[2] for con in connectionHistory[-len(range(int(math.sqrt(len(points)))+1, 1, -1)):]]
    
    plt.figure(figsize=(12, 12))
    
    plt.xlabel("Clusters amount")
    plt.ylabel("Shortest distance between 2 cluster centroids")
    plt.title("Hierarchical clusterization distance curve")
    
    plt.plot(X, Y, marker='o', color='blue')
    
    plt.show()
    
def HierarchicalSilhouettePlot(points):
    connectionHistory = HierarchicalClassifyPoints(points, points, isVisualized=False)
    
    X = [x for x in range(int(math.sqrt(len(points)))+1, 1, -1)]
    Y = [utils.GetSilhouetteScore(points, GetClusterizationFromHistory(connectionHistory, x)) for x in X]
    
    plt.figure(figsize=(12, 12))
    
    plt.xlabel("Clusters amount")
    plt.ylabel("Silhouette score")
    plt.title("Hierarchical clusterization silhouette score curve")
    
    plt.plot(X, Y, marker='o', color='blue', linestyle='')
    
    plt.show()