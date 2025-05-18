#
# 
#

import csv

vmin = [-1 for _ in range(21+8)] + [0]
vmax = [1 for _ in range(21+8+1)]

def MinMaxScaling():
    with open('data/phishing.data', 'r') as data, open('data/phishingScaled.data', 'w+') as dataScaled:
        
        reader = csv.reader(data, delimiter=',')
        
        for row in reader:
            rowA = [float((int(row[i])-vmin[i])/(vmax[i]-vmin[i])) for i in range(21+8+1)]
            for x in rowA:
                dataScaled.write(str(x))
                dataScaled.write(",")
            dataScaled.write(str(row[-1]) + '\n')
            
MinMaxScaling()