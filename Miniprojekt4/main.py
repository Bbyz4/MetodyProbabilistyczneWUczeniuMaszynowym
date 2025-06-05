import data_load as dl
import kmeans
import hierarchical
import spectral
import coolplots
import utils
import numpy as np
import matplotlib.pyplot as plt

import pandas as ps
import seaborn as sns

#(set, cluster amount)
""" discoveredClusterNumbers = [(2,6)]

for (dataID, amount) in discoveredClusterNumbers:
    
    print(f"Creating a plot for {(dataID, amount)}")
    
    points, classes = dl.Get2DPointData(dataID)
    
    kmeansclusters, _ = kmeans.KmeansClassifyPoints(points, points, k=amount, isVisualized=False, isPlusPlus=True, dataID=dataID)
    hierarchicalclusters = hierarchical.GetClusterizationFromHistory(hierarchical.HierarchicalClassifyPoints(points, points, isVisualized=False, dataID=dataID), desiredClusterNumber=amount)
    
    coolplots.CreateComparationPlot(points, classes, kmeansclusters, hierarchicalclusters) """
    


""" DATASET = [3]
CONSTRUCT_METHOD = [spectral.MatrixConstructMethod.FULL_RBF]
PARAMETER = [0.5,0.55,0.6]

for dataset in DATASET:
    for construct_method in CONSTRUCT_METHOD:
        for parameter in PARAMETER:
            points, classes = dl.Get2DPointData(dataset)

            k = len(set(classes))

            transformedPoints = spectral.SpectralTransformation(points, 3, True, construct_method, parameter)

            kmeansclusters, _ = kmeans.KmeansClassifyPoints(points, transformedPoints, k, isVisualized=False, isPlusPlus=True, dataID=dataset)
            hierarchicalclusters = hierarchical.GetClusterizationFromHistory(hierarchical.HierarchicalClassifyPoints(points, transformedPoints, isVisualized=False, dataID=dataset), desiredClusterNumber=k)

            coolplots.CreateComparationPlot(points, classes, kmeansclusters, hierarchicalclusters) """
           
points = dl.Get18PointData()

X = []
Y = []

transformedPoints = spectral.SpectralTransformation(points, desiredDimension=20, normalizedLaplacian=True, matrixMethod=spectral.MatrixConstructMethod.FULL_RBF, parameter=10)

hierarchical.HierarchicalDistancePlot(transformedPoints)
    
    
""" plt.figure(figsize=(12,12))
plt.plot(X, Y, marker='o', linestyle='')
plt.xscale("log")
plt.xlabel("K value")
plt.ylabel("Computed score")
plt.title("Spectral KNN")
plt.show() """
    
""" for i in [2]:
    points, classes = dl.Get2DPointData(i)
    
    kmeans.KmeansClassifyPoints(points, points, k=len(set(classes)), isVisualized=True, isPlusPlus=True, dataID=i) """
    
""" for j in [1,2,3,4,7,8]:
    points, classes = dl.Get2DPointData(j)
    
    hierarchical.HierarchicalClassifyPoints(points, points, isVisualized=True, dataID=j) """
    
""" points, classes = dl.GetRPData()
    
df = ps.DataFrame(points)
    
correlation_matrix_pearson = df.corr(method='pearson')

plt.figure(figsize=(12, 12)) 
sns.heatmap(correlation_matrix_pearson,
            annot=True,   
            cmap='coolwarm', 
            fmt=".2f",  
            linewidths=.5)

plt.title('Correlation Matrix of 18 Features (Pearson)', fontsize=16)
plt.show()


print("Pearson Correlation Matrix:")
print(correlation_matrix_pearson)  """