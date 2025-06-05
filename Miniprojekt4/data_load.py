#
#
#

import csv
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def Get2DPointData(fileID):
    points = []
    realClasses = []
    with open(f'data/dane_2D_{fileID}.txt') as dane:
        reader = csv.reader(dane, delimiter='\t')
        for row in reader:
            row = [float(f) for f in row]
            points.append(row[:-1])
            realClasses.append(row[-1])
            
    return points, realClasses

def Get18PointData():
    points = []
    with open(f'data/data_18D.txt') as dane:
        reader = csv.reader(dane, delimiter='\t')
        for row in reader:
            row = [float(f) for f in row]
            points.append(row)

    points.pop()
    points_np = np.array(points)
    scaler = MinMaxScaler()
    scaled_points = scaler.fit_transform(points_np)
    
    return list(scaled_points)

def GetRPData():
    points = []
    realClasses = []
    with open(f'data/rp.data') as dane:
        reader = csv.reader(dane, delimiter='\t')
        for row in reader:
            row = row[0].split()
            row = [float(f) for f in row]
            points.append(row[:-1])
            realClasses.append(row[-1])
            
    return points, realClasses