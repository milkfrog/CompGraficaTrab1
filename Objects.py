import numpy as np
from math import sin, cos

def objectCenter(obj: np.array):
    xColumn = obj[:, 0]
    yColumn = obj[:, 1]
    zColumn = obj[:, 2]
    n = len(obj[:, 0])
    x = sum(xColumn[i] for i in range(len(xColumn))) / n
    y = sum(yColumn[i] for i in range(len(yColumn))) / n
    z = sum(zColumn[i] for i in range(len(zColumn))) / n
    return np.array([x, y, z])


def viewUpVector(angle):
    return np.array([cos(angle), sin(angle)])


def viewRightVector(angle):
    return np.array([sin(angle), -cos(angle)])


def translateMatrix(d):
    tMatrix = np.array([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [d[0], d[1], d[2], 1]])
    return tMatrix


def rotateMatrix(theta, center: np.array):
    rMatrix = np.array([[cos(-theta), -sin(-theta), 0, 0],
                        [sin(-theta),  cos(-theta), 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])
    return translateMatrix(-1 * center) @ rMatrix @ translateMatrix(center)


def scaleMatrix(s, center: np.array):
    sMatrix = np.array([[s[0], 0, 0, 0],
                        [0, s[1], 0, 0],
                        [0, 0, s[2], 0],
                        [0, 0, 0, 1]])
    return translateMatrix(-1 * center) @ sMatrix @ translateMatrix(center)


def normalizationMatrix(window: np.array, windowRotation):
    tMatrix = translateMatrix(-1 * objectCenter(window))
    rMatrix = rotateMatrix(-windowRotation, np.array([0, 0, 0]))
    centeredWindow = window @ tMatrix @ rMatrix
    sMatrix = scaleMatrix([1 / centeredWindow[0, 0], 1 / centeredWindow[0, 1], 1], np.array([0, 0, 0]))
    return tMatrix @ rMatrix @ sMatrix


def transformViewPortX(Xw, Xwmin, Xwmax, Xvpmax, Xvpmin):
    return (Xw - Xwmin)/(Xwmax - Xwmin)*(Xvpmax - Xvpmin)


def transformViewPortY(Yw, Ywmin, Ywmax, Yvpmax, Yvpmin):
    return (1 - (Yw - Ywmin)/(Ywmax - Ywmin))*(Yvpmax - Yvpmin)


def transformViewPort(normalizedObjectCoordinates: np.array, wSize):

        if normalizedObjectCoordinates.ndim is 1:
            transformedCoordinates = np.array([[transformViewPortX(normalizedObjectCoordinates[0], -1, 1, wSize[0], 0),
                                               transformViewPortY(normalizedObjectCoordinates[1], -1, 1, wSize[1], 0),
                                               1,
                                               1]])
        elif normalizedObjectCoordinates.ndim is 2:
            transformedCoordinates = np.ones(normalizedObjectCoordinates.shape)
            for i in range(normalizedObjectCoordinates.shape[0]):
                transformedCoordinates[i, 0] = transformViewPortX(normalizedObjectCoordinates[i, 0], -1, 1, wSize[0], 0)
                transformedCoordinates[i, 1] = transformViewPortY(normalizedObjectCoordinates[i, 1], -1, 1, wSize[1], 0)
        else:
            # this is an error situation
            pass
        
        return transformedCoordinates