import numpy as np


def calcAngularError(predictedFlow, groundtruthFlow):
    numerator = 1.0 + predictedFlow[0]*groundtruthFlow[0] + predictedFlow[1]*groundtruthFlow[1]
    denominator = np.sqrt(1.0 + predictedFlow[0]**2 + predictedFlow[1]**2) * np.sqrt(1.0 + groundtruthFlow[0]**2 + groundtruthFlow[1]**2)
    return np.arccos(numerator / denominator)


def calcAngularErrorForEachPixel(predictedFlowArray, groundtruthFlowArray):
    performance = []
    for predictedFlow, groundtruthFlow in zip(predictedFlowArray, groundtruthFlowArray):
        performance.append(calcAngularError(predictedFlow, groundtruthFlow))
    return performance


def calcEndpointError(predictedFlow, groundtruthFlow):
    return np.linalg.norm(predictedFlow - groundtruthFlow)


def calcEndpointErrorForEachPixel(predictedFlowArray, groundtruthFlowArray):
    performance = []
    for predictedFlow, groundtruthFlow in zip(predictedFlowArray, groundtruthFlowArray):
        performance.append(calcEndpointError(predictedFlow, groundtruthFlow))
    return performance


def getFlowErrorAverage(errorsInOneFrame):
    return np.mean(errorsInOneFrame)


def getFlowErrorStandardDeviation(errorsInOneFrame):
    return np.std(errorsInOneFrame)


def sortAscending(errorsInOneFrame):
    return np.sort(errorsInOneFrame)


def getPercentageOfErrorOverThreshold(sortedErrorsInOneFrame, threshold):
    numAllPixels = sortedErrorsInOneFrame.size()
    numPixelsWithErrorLargerThanThreshold = np.searchsorted(sortedErrorsInOneFrame, threshold, side='left')
    return (numPixelsWithErrorLargerThanThreshold / numAllPixels) * 100.0


def getErrorAtNthPercentiles(errorsInOneFrame, nthPercentiles):
    return np.percentile(errorsInOneFrame, nthPercentiles)
