import numpy as np
import math

def GetDistinctRealClassesAmount(realClasses):
    return len(set(realClasses))

def EuclideanDistSquared(p1, p2):
    return sum((x-y)**2 for x,y in zip(p1, p2))

def NormalizeClassification(classification):
    return [len(set(cla for cla in classification if cla<classification[j])) for j in range(len(classification))]

def GetSilhouetteScore(points, pointClusters):
    normalizedPointsClasses = NormalizeClassification(pointClusters)
    
    centroids = [np.mean([points[k] for k in range(len(points)) if normalizedPointsClasses[k]==cla], axis=0) for cla in range(len(set(normalizedPointsClasses)))]
    
    a = [EuclideanDistSquared(points[i], centroids[normalizedPointsClasses[i]]) for i in range(len(points))]
    b = [min(EuclideanDistSquared(points[i], centroids[j]) for j in range(len(centroids)) if j!=normalizedPointsClasses[i]) for i in range(len(points))]
            
    return (1/len(points))*sum((b[i]-a[i])/(max(b[i], a[i])) for i in range(len(points)))

def CalculateClusterizationScore(realClasses, computedClasses):
    
    c1 = NormalizeClassification(realClasses)
    c2 = NormalizeClassification(computedClasses)
    
    n = len(realClasses)
    
    return (1/(n*(n-1))) * sum(1 for i in range(n) for j in  range(n) if 
    ((i != j) and
     ((realClasses[i]==realClasses[j]),(computedClasses[i]==computedClasses[j])) in [(True, True), (False, False)]))
    
def GetPotentialGamma(points):
    n = len(points)
    
    argSum = 0
    
    for i in range(n):
        closestPointsIndeces = np.argsort([EuclideanDistSquared(points[i], points[j]) for j in range(n)])
        
        argSum += EuclideanDistSquared(points[closestPointsIndeces[int(math.sqrt(n))]], points[i])/n
        
    return (1/(2*(argSum**2)))