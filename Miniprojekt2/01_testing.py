from logistic_regression import GetDecisiveFunction
import data_split as ds

trainingSet, _ = ds.GetDataSplit()
func = GetDecisiveFunction(trainingSet, 1000, 0.1)