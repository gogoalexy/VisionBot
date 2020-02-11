import math
import numpy as np

shiftScale = 0.04
zoomScale = 2.5
rotateScale = 1.5

def createCamLeftShiftTemplate(height, width):
    template = np.empty((height, width, 2))
    for y in range(0, height):
        for x in range(0, width):
            template[y][x][0] = 1.0 * shiftScale
            template[y][x][1] = 0.0
    return template

def createCamRightShiftTemplate(height, width):
    template = np.empty((height, width, 2))
    for y in range(0, height):
        for x in range(0, width):
            template[y][x][0] = -1.0 * shiftScale
            template[y][x][1] = 0.0
    return template

def createCamUpShiftTemplate(height, width):
    template = np.empty((height, width, 2))
    for y in range(0, height):
        for x in range(0, width):
            template[y][x][0] = 0.0
            template[y][x][1] = 1.0 * shiftScale
    return template

def createCamDownShiftTemplate(height, width):
    template = np.empty((height, width, 2))
    for y in range(0, height):
        for x in range(0, width):
            template[y][x][0] = 0.0
            template[y][x][1] = -1.0 * shiftScale
    return template

def createCamZoomInTemplate(height, width):
    template = np.empty((height, width, 2))
    center = (height/2.0, width/2.0)
    for y in range(0, height):
        j = y - center[0]
        for x in range(0, width):
            i = x - center[1]
            norm = (i**2 + j**2)
            if norm < 0.01:
                norm = 0.1
            if norm < 3.0:
                template[y][x][0] = 2*zoomScale * i/norm
                template[y][x][1] = 2*zoomScale * j/norm
            else:
                template[y][x][0] = zoomScale * i/norm
                template[y][x][1] = zoomScale * j/norm

    return template

def createCamZoomOutTemplate(height, width):
    template = np.empty((height, width, 2))
    center = (height/2.0, width/2.0)
    for y in range(0, height):
        j = y - center[0]
        for x in range(0, width):
            i = x - center[1]
            norm = (i**2 + j**2)
            if norm < 0.01:
                norm = 0.1
            if norm < 3.0:
                template[y][x][0] = 2*zoomScale * -i/norm
                template[y][x][1] = 2*zoomScale * -j/norm
            else:
                template[y][x][0] = zoomScale * -i/norm
                template[y][x][1] = zoomScale * -j/norm

    return template

def createCamRotateCWTemplate(height, width):
    template = np.empty((height, width, 2))
    center = (height/2.0, width/2.0)
    for y in range(0, height):
        j = y - center[0]
        for x in range(0, width):
            i = x - center[1]
            norm = (i**2 + j**2)
            if norm < 0.01:
                norm = 0.1
            template[y][x][0] = rotateScale * j/norm
            template[y][x][1] = rotateScale * -i/norm
    return template

def createCamRotateCCWTemplate(height, width):
    template = np.empty((height, width, 2))
    center = (height/2.0, width/2.0)
    for y in range(0, height):
        j = y - center[0]
        for x in range(0, width):
            i = x - center[1]
            norm = (i**2 + j**2)
            if norm < 0.01:
                norm = 0.1
            template[y][x][0] = rotateScale * -j/norm
            template[y][x][1] = rotateScale * i/norm
    return template

def createAvoidFrontTemplate(height, width):
    template = np.empty((height, width, 2))
    center = (height/2.0, width/2.0)
    template = createCamZoomInTemplate(height, width) * 6
    for y in range(0, height):
        j = y - center[0]
        for x in range(0, width):
            i = x - center[1]
            norm = math.sqrt(i**2 + j**2)
            if norm < 14:
                template[y][x][0] = - template[y][x][0]
                template[y][x][1] = - template[y][x][1]
            if j < -1:
                if x>16 and x<47:
                    template[y][x][0] = template[y][x][0]
                    template[y][x][1] = template[y][x][1]
    return template

def createAvoidRearTemplate(height, width):
    template = np.empty((height, width, 2))
    center = (height/2.0, width/2.0)
    template = createCamZoomInTemplate(height, width) * 6
    for y in range(0, height):
        j = y - center[0]
        for x in range(0, width):
            i = x - center[1]
            norm = math.sqrt(i**2 + j**2)
            if norm < 14:
                template[y][x][0] = - template[y][x][0]
                template[y][x][1] = - template[y][x][1]
            if j > 1:
                if x>16 and x<47:
                    template[y][x][0] = template[y][x][0]
                    template[y][x][1] = template[y][x][1]
    return template

def createAvoidLeftTemplate(height, width):
    template = np.empty((height, width, 2))
    center = (height/2.0, width/2.0)
    template = createCamZoomInTemplate(height, width) * 6
    for y in range(0, height):
        j = y - center[0]
        for x in range(0, width):
            i = x - center[1]
            norm = math.sqrt(i**2 + j**2)
            if norm < 14:
                template[y][x][0] = - template[y][x][0]
                template[y][x][1] = - template[y][x][1]
            if i < -1:
                if y>16 and y<47:
                    template[y][x][0] = template[y][x][0]
                    template[y][x][1] = template[y][x][1]
    return template

def createAvoidRightTemplate(height, width):
    template = np.empty((height, width, 2))
    center = (height/2.0, width/2.0)
    template = createCamZoomInTemplate(height, width) * 6
    for y in range(0, height):
        j = y - center[0]
        for x in range(0, width):
            i = x - center[1]
            norm = math.sqrt(i**2 + j**2)
            if norm < 14:
                template[y][x][0] = - template[y][x][0]
                template[y][x][1] = - template[y][x][1]
            if i > 1:
                if y>16 and y<47:
                    template[y][x][0] = template[y][x][0]
                    template[y][x][1] = template[y][x][1]
    return template

def createAllFlattenTemplate(height, width):
    print("The function -createAllFlattenTemplate- is depricated. You may want to use -readAllFlattenTemplate- instead.")
    allTemplates = []
    allTemplates.append(createCamRotateCWTemplate(height, width).flatten())
    allTemplates.append(createCamRotateCCWTemplate(height, width).flatten())
    allTemplates.append(createCamZoomInTemplate(height, width).flatten())
    allTemplates.append(createCamZoomOutTemplate(height, width).flatten())
    allTemplates.append(createCamDownShiftTemplate(height, width).flatten())
    allTemplates.append(createCamUpShiftTemplate(height, width).flatten())
    allTemplates.append(createCamRightShiftTemplate(height, width).flatten())
    allTemplates.append(createCamLeftShiftTemplate(height, width).flatten())
    # allTemplates.append(createAvoidRearTemplate(height, width).flatten())
    # allTemplates.append(createAvoidFrontTemplate(height, width).flatten())
    # allTemplates.append(createAvoidLeftTemplate(height, width).flatten())
    # allTemplates.append(createAvoidRightTemplate(height, width).flatten())
    return allTemplates

def readAllFlattenTemplate_old():
    xfile = open("assets/matricesX.txt", 'r')
    yfile = open("assets/matricesY.txt", 'r')
    Fields = [ [], [], [], [], [], [], [], [] ]
    for xline, yline in zip(xfile, yfile):
        xmotions = xline.split()
        ymotions = yline.split()
        for container, xelement, yelement in zip(Fields, xmotions, ymotions):
            container.append(float(xelement))
            container.append(float(yelement))
    for container in Fields:
      container = np.array(container)
    return Fields

def readAllFlattenTemplate():
    xfile = open("assets/ExternalSynapse_X.txt", 'r')
    yfile = open("assets/ExternalSynapse_Y.txt", 'r')
    Fields = [ [], [], [], [] ]
    for xline, yline in zip(xfile, yfile):
        xmotions = xline.split()
        ymotions = yline.split()
        for container, xelement, yelement in zip(Fields, xmotions, ymotions):
            container.append(float(xelement))
            container.append(float(yelement))
    for container in Fields:
        container = np.array(container)
    return Fields

def dotWithTemplatesOpt_old(tobeDotted, templates):
    results = []
    for template in templates:
        results.append(np.inner(tobeDotted, template))
    results.insert(1, -results[0])
    results.insert(3, -results[2])
    results.insert(5, -results[4])
    results.insert(7, -results[6])
    for index in range(8, 12):
          results[index] = np.abs(results[index])
    return results

def dotWithTemplatesOpt(tobeDotted, templates):
    results = []
    for template in templates:
        results.append(np.inner(tobeDotted, template))
    results.insert(1, -results[0])
    results.insert(3, -results[2])
    results.insert(5, -results[4])
    results.insert(7, -results[6])
    return results

def dotWithTemplates(tobeDotted, templates):
    print("The function -dotWithTemplates- is depricated. Use it with -createAllFlattenTemplates- only.")
    results = []
    for template in templates:
        results.append(np.inner(tobeDotted, template))
    return results

def meanOpticalFlow(flow):
    '''
    for j in range(0, 63, 8):
        for i in range(0, 63, 8):
            x = flow[j:j+8, i:i+8, 0]
            y = flow[j:j+8, i:i+8, 1]
            mean[0][j//8][i//8] = np.mean(x)
            mean[1][j//8][i//8] = np.mean(y)
    '''
    flowX = flow[:, :, 0]
    flowY = flow[:, :, 1]
    #shape = (8, 8)
    #sh = shape[0],flow.shape[0]//shape[0],shape[1],flow.shape[1]//shape[1]
    sh = (8, 8, 8, 8)
    meanFlowX = flowX.reshape(sh).mean(-1).mean(1)
    meanFlowY = flowY.reshape(sh).mean(-1).mean(1)
    meanFlow = np.dstack((meanFlowX, meanFlowY))
    return meanFlow

def obstacleAvoidanceCurrent(flow, templates):
    neuronCurrent = []
    return neuronCurrent

