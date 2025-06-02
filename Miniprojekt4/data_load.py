#
#
#

import csv

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

def Get18PointData(fileID):
    points = []
    realClasses = []
    with open(f'data/dane_18.txt') as dane:
        reader = csv.reader(dane, delimiter='\t')
        for row in reader:
            row = [float(f) for f in row]
            points.append(row[:-1])
            realClasses.append(row[-1])
            
    return points, realClasses

def GetRPData(fileID):
    points = []
    realClasses = []
    with open(f'data/rp.data') as dane:
        reader = csv.reader(dane, delimiter='\t')
        for row in reader:
            row = [float(f) for f in row]
            points.append(row[:-1])
            realClasses.append(row[-1])
            
    return points, realClasses