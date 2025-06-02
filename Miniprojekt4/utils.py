def GetDistinctRealClassesAmount(realClasses):
    return len(set(realClasses))

def EuclideanDistSquared(p1, p2):
    return sum((x-y)**2 for x,y in zip(p1, p2))