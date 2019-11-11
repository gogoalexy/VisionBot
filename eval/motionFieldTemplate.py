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
        for x in range(0, width):
            j = y - center[0]
            i = x - center[1]
            norm = (i**2 + j**2)
            if norm < 0.1:
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
        for x in range(0, width):
            j = y - center[0]
            i = x - center[1]
            norm = (i**2 + j**2)
            if norm < 0.1:
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
        for x in range(0, width):
            j = y - center[0]
            i = x - center[1]
            norm = (i**2 + j**2)
            if norm < 0.1:
                norm = 0.1
            template[y][x][0] = rotateScale * j/norm
            template[y][x][1] = rotateScale * -i/norm
    return template

def createCamRotateCCWTemplate(height, width):
    template = np.empty((height, width, 2))
    center = (height/2.0, width/2.0)
    for y in range(0, height):
        for x in range(0, width):
            j = y - center[0]
            i = x - center[1]
            norm = (i**2 + j**2)
            if norm < 0.1:
                norm = 0.1
            template[y][x][0] = rotateScale * -j/norm
            template[y][x][1] = rotateScale * i/norm
    return template

# Order: UP, DOWN, LEFT, RIGHT, ZOOMIN, ZOOMOUT, ROTATECW, ROTATECCW
def createAllFlattenTemplate(height, width):
    allTemplates = []
    allTemplates.append(createCamUpShiftTemplate(height, width).flatten())
    allTemplates.append(createCamDownShiftTemplate(height, width).flatten())
    allTemplates.append(createCamLeftShiftTemplate(height, width).flatten())
    allTemplates.append(createCamRightShiftTemplate(height, width).flatten())
    allTemplates.append(createCamZoomInTemplate(height, width).flatten())
    allTemplates.append(createCamZoomOutTemplate(height, width).flatten())
    allTemplates.append(createCamRotateCWTemplate(height, width).flatten())
    allTemplates.append(createCamRotateCCWTemplate(height, width).flatten())
    return allTemplates

def dotWithTemplates(tobeDotted, templates):
    results = []
    for template in templates:
        results.append(np.inner(tobeDotted, template))
    return results
