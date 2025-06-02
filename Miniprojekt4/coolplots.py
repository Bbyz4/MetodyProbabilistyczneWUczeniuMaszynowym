import matplotlib.pyplot as plt
import numpy as np
import colorsys
import random
import math

from matplotlib.animation import FuncAnimation

def GenerateRainbowColors(n):
    return [
        '#{:02x}{:02x}{:02x}'.format(*[int(c * 255) for c in colorsys.hsv_to_rgb(i / n, 1, 1)]) for i in range(n)
    ]

def PlotKmeansIterations(pointPositions, pointKeyframeData, centroidKeyframeData, framesPerTransition = 60, blinkFrames = 20, dataID = 0):
    
    fig, ax = plt.subplots(figsize= (12,12))
    
    plt.title(f"Kmeans algorithm visualization for dane_2D_{dataID}")
    
    totalFrames = framesPerTransition * (len(centroidKeyframeData) + len(pointKeyframeData) - 2)
    
    pointPositions = np.array(pointPositions)
    pointKeyframeData = np.array(pointKeyframeData)
    centroidKeyframeData = np.array(centroidKeyframeData)
    
    max_coeff = max([pointPositions[i][0] for i in range(len(pointPositions))] + [pointPositions[i][1] for i in range(len(pointPositions))])
    min_coeff = min([pointPositions[i][0] for i in range(len(pointPositions))] + [pointPositions[i][1] for i in range(len(pointPositions))])
    
    ax.set_xlim(min_coeff*1.1, max_coeff*1.1)
    ax.set_ylim(min_coeff*1.1, max_coeff*1.1)
    
    colors = GenerateRainbowColors(len(set(pointKeyframeData[0])))
    
    pointScatterplot = ax.scatter(pointPositions[:, 0], pointPositions[:, 1], s=50, c='black')
    centroidScatterplot = ax.scatter(centroidKeyframeData[0][:, 0], centroidKeyframeData[0][:, 1], s=75, c=colors, zorder=2)
    centroidHullScatterplot = ax.scatter(centroidKeyframeData[0][:, 0], centroidKeyframeData[0][:, 1], s=150, c='black', zorder=1)
    
    def init():
        centroidScatterplot.set_offsets(centroidKeyframeData[0])
        centroidHullScatterplot.set_offsets(centroidKeyframeData[0])
        return( centroidScatterplot, )
    
    def animate(i):
        alpha = (i%framesPerTransition)/framesPerTransition
        currentTransition = int(i/framesPerTransition)
        
        if currentTransition % 2 == 1 :
            centroidScatterplot.set_offsets(centroidKeyframeData[int(currentTransition/2)] * (1-alpha) + centroidKeyframeData[int(currentTransition/2) + 1] * (alpha))
            centroidHullScatterplot.set_offsets(centroidKeyframeData[int(currentTransition/2)] * (1-alpha) + centroidKeyframeData[int(currentTransition/2) + 1] * (alpha))
            return (centroidScatterplot, centroidHullScatterplot)
        else:
            if int(currentTransition/2) == 0:  
                pointScatterplot.set_color([colors[pointKeyframeData[int(currentTransition/2)][i]] for i in range(len(pointPositions))] if i%blinkFrames > (blinkFrames/2) else ['black' for i in range(len(pointPositions))])
            else:
                pointScatterplot.set_color([colors[pointKeyframeData[int(currentTransition/2)][i]] for i in range(len(pointPositions))] if i%blinkFrames > (blinkFrames/2) else [colors[pointKeyframeData[int(currentTransition/2)-1][i]] for i in range(len(pointPositions))])
            return (pointScatterplot, )
            
    
    anim = FuncAnimation(
        fig,
        animate,
        init_func= init,
        frames= totalFrames,
        interval = 10,
        blit = True,
        repeat = True)
    
    anim.save(f'videos/random_{dataID}.mp4', fps=120)
    
def PlotKmeansIterationsAfterMapping(originalPoints, transformedPoints, pointKeyframeData, centroidKeyframeData, framesPerTransition = 60, blinkFrames = 20, dataID = 0):
    
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(24,12))
    
    ax1.set_title("Plot 1")
    ax2.set_title("Plot 2")
    
    totalFrames = framesPerTransition * (len(centroidKeyframeData) + len(pointKeyframeData) - 2)
    
    originalPoints = np.array(originalPoints)
    transformedPoints = np.array(transformedPoints)
    pointKeyframeData = np.array(pointKeyframeData)
    centroidKeyframeData = np.array(centroidKeyframeData)
    
    max_coeff_1 = max([originalPoints[i][0] for i in range(len(originalPoints))] + [originalPoints[i][1] for i in range(len(originalPoints))])
    min_coeff_1 = min([originalPoints[i][0] for i in range(len(originalPoints))] + [originalPoints[i][1] for i in range(len(originalPoints))])
    
    ax1.set_xlim(min_coeff_1*1.1, max_coeff_1*1.1)
    ax1.set_ylim(min_coeff_1*1.1, max_coeff_1*1.1)
    
    max_coeff_2 = max([transformedPoints[i][0] for i in range(len(transformedPoints))] + [transformedPoints[i][1] for i in range(len(transformedPoints))])
    min_coeff_2 = min([transformedPoints[i][0] for i in range(len(transformedPoints))] + [transformedPoints[i][1] for i in range(len(transformedPoints))])
    
    ax2.set_xlim(min_coeff_2*1.1, max_coeff_2*1.1)
    ax2.set_ylim(min_coeff_2*1.1, max_coeff_2*1.1)
    
    colors = GenerateRainbowColors(len(set(pointKeyframeData[0])))
    
    originalPointScatterplot = ax1.scatter(originalPoints[:, 0], originalPoints[:, 1], s=50, c='black')
    
    pointScatterplot = ax2.scatter(transformedPoints[:, 0], transformedPoints[:, 1], s=50, c='black')
    centroidScatterplot = ax2.scatter(centroidKeyframeData[0][:, 0], centroidKeyframeData[0][:, 1], s=75, c=colors, zorder=2)
    centroidHullScatterplot = ax2.scatter(centroidKeyframeData[0][:, 0], centroidKeyframeData[0][:, 1], s=150, c='black', zorder=1)
    
    def init():
        centroidScatterplot.set_offsets(centroidKeyframeData[0])
        centroidHullScatterplot.set_offsets(centroidKeyframeData[0])
        return( centroidScatterplot, )
    
    def animate(i):
        alpha = (i%framesPerTransition)/framesPerTransition
        currentTransition = int(i/framesPerTransition)
        
        if currentTransition % 2 == 1 :
            centroidScatterplot.set_offsets(centroidKeyframeData[int(currentTransition/2)] * (1-alpha) + centroidKeyframeData[int(currentTransition/2) + 1] * (alpha))
            centroidHullScatterplot.set_offsets(centroidKeyframeData[int(currentTransition/2)] * (1-alpha) + centroidKeyframeData[int(currentTransition/2) + 1] * (alpha))
            return (centroidScatterplot, centroidHullScatterplot)
        else:
            if int(currentTransition/2) == 0:  
                pointScatterplot.set_color([colors[pointKeyframeData[int(currentTransition/2)][i]] for i in range(len(transformedPoints))] if i%blinkFrames > (blinkFrames/2) else ['black' for i in range(len(transformedPoints))])
                originalPointScatterplot.set_color([colors[pointKeyframeData[int(currentTransition/2)][i]] for i in range(len(originalPoints))] if i%blinkFrames > (blinkFrames/2) else ['black' for i in range(len(originalPoints))])
            else:
                pointScatterplot.set_color([colors[pointKeyframeData[int(currentTransition/2)][i]] for i in range(len(transformedPoints))] if i%blinkFrames > (blinkFrames/2) else [colors[pointKeyframeData[int(currentTransition/2)-1][i]] for i in range(len(transformedPoints))])
                originalPointScatterplot.set_color([colors[pointKeyframeData[int(currentTransition/2)][i]] for i in range(len(originalPoints))] if i%blinkFrames > (blinkFrames/2) else [colors[pointKeyframeData[int(currentTransition/2)-1][i]] for i in range(len(originalPoints))])
            return (pointScatterplot, originalPointScatterplot)
            
    
    anim = FuncAnimation(
        fig,
        animate,
        init_func= init,
        frames= totalFrames,
        interval = 10,
        blit = True,
        repeat = True)
    
    anim.save(f'videos/random_{dataID}.mp4', fps=120)
 
# For maintaining cluster connections
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        
    def find(self, i):
        if self.parent[i] == i:
            return i
        else:
            self.parent[i] = self.find(self.parent[i])
            return self.parent[i]
        
    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        
        if root_i != root_j:
            if self.size[root_i] > self.size[root_j]:
                root_i, root_j = root_j, root_i
                
            self.parent[root_i] = root_j
            self.size[root_j] += self.size[root_i]
            return True
        else:
            return False
    
    
def PlotHierarchicalHistory(points, connectionHistory, dataID = 0):
    
    fig, ax = plt.subplots(figsize=(12,12))
    
    totalFrames = int(math.sqrt(len(points))) * 30 + int(len(points) - math.sqrt(len(points)))
    
    plt.title(f"Hierarchical clustering visualization for dane_2D_{dataID}")
    
    max_coeff = max([points[i][0] for i in range(len(points))] + [points[i][1] for i in range(len(points))])
    min_coeff = min([points[i][0] for i in range(len(points))] + [points[i][1] for i in range(len(points))])
    
    ax.set_xlim(min_coeff*1.1, max_coeff*1.1)
    ax.set_ylim(min_coeff*1.1, max_coeff*1.1)
    
    clusterColors = GenerateRainbowColors(len(points))
    random.shuffle(clusterColors)
    
    pointScatterplot = ax.scatter([points[i][0] for i in range(len(points))], [points[i][1] for i in range(len(points))], s=50, c=clusterColors)
    
    frame_text = ax.text(0.02, 0.98, '', transform=ax.transAxes,
                            ha='left', va='top', fontsize=16,
                            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))
    
    D = DSU(2*len(points))
    currentConnection = 0
    currentI = 0
    
    def init():
        nonlocal currentConnection
        
        frame_text.set_text(f"{len(points) - currentConnection}")
        return (pointScatterplot, frame_text)
    
    #Until sqrt(len(points)) - 1 frame per connection
    #After sqrt(len(points)) - 30 frames per connection
    def animate(i):
        nonlocal currentConnection, currentI
        
        if (len(points) - currentConnection > math.sqrt(len(points)) or currentI == 30) and currentConnection < len(points):
            D.union(connectionHistory[currentConnection][0][0], connectionHistory[currentConnection][0][1])
            D.union(connectionHistory[currentConnection][0][0], len(points) + currentConnection)
            currentConnection += 1 
            currentI = 0
            
            pointScatterplot.set_color([clusterColors[D.find(i)] for i in range(len(points))])
            frame_text.set_text(f"{len(points) - currentConnection}")
            
            return (pointScatterplot, frame_text)
        else:
            currentI += 1 
            return tuple()

    anim = FuncAnimation(
        fig,
        animate,
        init_func= init,
        frames= totalFrames,
        interval = 1,
        blit = True,
        repeat = True)
    
    anim.save(f'videos/fandom_{dataID}.mp4', fps=60)
    
def PlotHierarchicalHistoryAfterMapping(originalPoints, points, connectionHistory, dataID = 0):

    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(24,12))
    
    ax1.set_title("Plot 1")
    ax2.set_title("Plot 2")

    totalFrames = int(math.sqrt(len(points))) * 30 + int(len(points) - math.sqrt(len(points)))

    plt.title(f"Hierarchical clustering visualization for dane_2D_{dataID}")

    max_coeff2 = max([points[i][0] for i in range(len(points))] + [points[i][1] for i in range(len(points))])
    min_coeff2 = min([points[i][0] for i in range(len(points))] + [points[i][1] for i in range(len(points))])

    ax2.set_xlim(min_coeff2*1.1, max_coeff2*1.1)
    ax2.set_ylim(min_coeff2*1.1, max_coeff2*1.1)

    clusterColors = GenerateRainbowColors(len(points))
    random.shuffle(clusterColors)

    originalPointScatterplot = ax1.scatter([originalPoints[i][0] for i in range(len(originalPoints))], [originalPoints[i][1] for i in range(len(originalPoints))], s=50, c=clusterColors)
    pointScatterplot = ax2.scatter([points[i][0] for i in range(len(points))], [points[i][1] for i in range(len(points))], s=50, c=clusterColors)

    frame_text = ax2.text(0.02, 0.98, '', transform=ax2.transAxes,
                            ha='left', va='top', fontsize=16,
                            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))

    D = DSU(2*len(points))
    currentConnection = 0
    currentI = 0

    def init():
        nonlocal currentConnection
        
        frame_text.set_text(f"{len(points) - currentConnection}")
        return (pointScatterplot, frame_text)

    #Until sqrt(len(points)) - 1 frame per connection
    #After sqrt(len(points)) - 30 frames per connection
    def animate(i):
        nonlocal currentConnection, currentI
        
        if (len(points) - currentConnection > math.sqrt(len(points)) or currentI == 30) and currentConnection < len(points):
            D.union(connectionHistory[currentConnection][0][0], connectionHistory[currentConnection][0][1])
            D.union(connectionHistory[currentConnection][0][0], len(points) + currentConnection)
            currentConnection += 1 
            currentI = 0
            
            pointScatterplot.set_color([clusterColors[D.find(i)] for i in range(len(points))])
            originalPointScatterplot.set_color([clusterColors[D.find(i)] for i in range(len(originalPoints))])
            frame_text.set_text(f"{len(points) - currentConnection}")
            
            return (pointScatterplot, originalPointScatterplot, frame_text)
        else:
            currentI += 1 
            return tuple()

    anim = FuncAnimation(
        fig,
        animate,
        init_func= init,
        frames= totalFrames,
        interval = 1,
        blit = True,
        repeat = True)

    anim.save(f'videos/fandom_{dataID}.mp4', fps=60)