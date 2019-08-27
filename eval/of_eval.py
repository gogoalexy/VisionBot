import numpy as np
    
def calcAngularError(predictedFlow, groundtruthFlow):
    numerator = 1.0 + predictedFlow[0]*groundtruthFlow[0] + predictedFlow[1]*groundtruthFlow[1]
    denominator = np.sqrt(1.0 + predictedFlow[0]**2 + predictedFlow[1]**2) * np.sqrt(1.0 + groundtruthFlow[0]**2 + groundtruthFlow[1]**2)
    return np.arccos(numerator / denominator)

def calcAngularErrorForEachPixel(1DpredictedFlow, 1DgroundtruthFlow):
    performance = []
    for predictedFlow, groundtruthFlow in zip(1DpredictedFlow, 1DgroundtruthFlow):
        performance.append(clacAngularError(predictedFlow, groundtruthFlow))
    return performance

def calcEndpointError(predictedFlow, groundtruthFlow):
    return np.linalg.norm(predictedFlow - groundtruthFlow)

def calcEndpointErrorForEachPixel(1DpredictedFlow, 1DgroundtruthFlow):
    performance = []
    for predictedFlow, groundtruthFlow in zip(1DpredictedFlow, 1DgroundtruthFlow):
        performance.append(clacEndpointError(predictedFlow, groundtruthFlow))
    return performance

def getFlowErrorAverage(errorsInOneFrame):
    return np.mean(errorsInOneFrame)

def getFlowErrorStandardDeviation(errorsInOneFrame):
    return np.std(errorsInOneFrame)

def sortFromSmall2Large(errorsInOneFrame):
    return np.sort(errorsInOneFrame)

def getPercentageOfErrorOverThreshold(sortedErrorsInOneFrame, threshold):
    
