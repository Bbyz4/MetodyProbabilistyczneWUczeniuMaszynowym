import matplotlib.pyplot as plt
import csv

data_features = {}

def _PlotFeatures():
    
    featureNumber = len(data_features)
    cols = 4
    rows = -(-featureNumber // cols)
    
    fig, axes = plt.subplots(rows, cols, figsize=(20,10))
    axes = axes.flatten()
    
    for i, (key, value) in enumerate(data_features.items()):
        axes[i].violinplot(value)
        axes[i].set_title(key)

    plt.show()

def _ScaleData():
    
    for (key, value) in data_features.items():
        vmin = min(value)
        vmax = max(value)
        
        print(vmin, vmax)
        
        value = [(v - vmin)/(vmax - vmin) for v in value]
        
        data_features[key] = value

def _ReadData():
    
    with open('dane.data', 'r') as dataToScale:
        
        #Read the data and separate it by the features
        reader = csv.reader(dataToScale, delimiter='\t')
        
        for row in reader:
            for i, value in enumerate(row):
                if len(data_features) <= i:
                    data_features[f"Feature {i}"] = []
                value = value.replace(',', '.') #for easier conversion
                data_features[f"Feature {i}"].append(float(value))
    
def _SaveScaledData():
    
    with open('daneScaled.data', 'w') as dataScaled:
        for i in range(len(data_features["Feature 0"])):
            for j, key in enumerate(data_features.keys()):
                dataScaled.write(str(data_features[key][i]))
                dataScaled.write("\t" if j < len(data_features)-1 else "\n")
                
                
def Main(showPlots = False):
    _ReadData()
    if showPlots: _PlotFeatures()
    _ScaleData()
    #_SaveScaledData()
    
Main()