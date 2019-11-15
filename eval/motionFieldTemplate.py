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
    allTemplates = []
    allTemplates.append(createCamRotateCWTemplate(height, width).flatten())
    allTemplates.append(createCamRotateCCWTemplate(height, width).flatten())
    allTemplates.append(createCamZoomInTemplate(height, width).flatten())
    allTemplates.append(createCamZoomOutTemplate(height, width).flatten())
    allTemplates.append(createCamDownShiftTemplate(height, width).flatten())
    allTemplates.append(createCamUpShiftTemplate(height, width).flatten())
    allTemplates.append(createCamRightShiftTemplate(height, width).flatten())
    allTemplates.append(createCamLeftShiftTemplate(height, width).flatten())
    allTemplates.append(createAvoidRearTemplate(height, width).flatten())
    allTemplates.append(createAvoidFrontTemplate(height, width).flatten())
    allTemplates.append(createAvoidLeftTemplate(height, width).flatten())
    allTemplates.append(createAvoidRightTemplate(height, width).flatten())
    return allTemplates

def readAllFlattenTemplate():
    allTemplates = []
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
    results = []
    for template in templates:
        results.append(np.inner(tobeDotted, template))
    return results
