import numpy as np
from math import sin, cos

# A point is simply an array [x,y]
# A line is an array of 2 points [pointA,pointB]
# A polygon is an array of N points [[x1,y1],[x2,y2],[x3,y3] . . .]


class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.z = 1.0
    
    def __str__(self):
        return str(self.x) + ',' + str(self.y)


class Objeto:
    def __init__(self, name, worldCoordinates: np.array, tipo, quantidade):
        self.name = name
        self.worldCoordinates = worldCoordinates
        self.windowCoordinates = worldCoordinates
        self.tipo = tipo
        self.quantidade = quantidade


    def transformWorldCoordinates(self, tMatrix, windowTransform):
        self.worldCoordinates = self.worldCoordinates * tMatrix
        self.windowCoordinates = self.worldCoordinates * windowTransform

    def trasformWindowCoordinates(self, tMatrix, windowTransform):
        self.windowTransform = self.windowTransform * tMatrix
        self.windowCoordinates = self.worldCoordinates * windowTransform

    def resetWindowCoordinates(self, windowTransform):
        self.windowCoordinates = self.worldCoordinates
        self.windowCoordinates = windowTransform

    def bringToWorldCenter(self, windowTransform):
        objCenter = self.center()
        self.worldCoordinates = self.worldCoordinates * translateMatrix(-objCenter)
        self.windowCoordinates = self.worldCoordinates * windowTransform

    def translate(self, d, windowTransform):
        self.worldCoordinates = self.worldCoordinates * translateMatrix(d)
        self.windowCoordinates = self.worldCoordinates * windowTransform

    def rotate(self, theta, center, windowTransform):
        self.worldCoordinates = self.worldCoordinates * rotateMatrix(theta, center)
        self.windowCoordinates = self.worldCoordinates * windowTransform

    def scale(self, s, windowTransform):
        self.worldCoordinates = self.worldCoordinates * scaleMatrix(s, self.center())
        self.windowCoordinates = self.worldCoordinates * windowTransform

    
    # TODO: deixar bonito o print pra aparecer na listagem direito
    # def __str__(self):
    #     stringCoordenadas = "["
    #     for i in coordenates:
    #         stringCoordenadas += 
    #     return self.name + "(" + self.tipo + ") coordenadas = " + 

def objectCenter(obj: np.array):
    xColumns = obj[:, 0]
    yColumns = obj[:, 1]
    n = len(obj[:, 0])
    x = sum(xColumns[i] for i in range(len(xColumns))) / n
    y = sum(yColumns[i] for i in range(len(yColumns))) / n
    return np.array([x, y])


def viewUpVector(angle):
    return np.array([cos(angle), sin(angle)])


def viewRightVector(angle):
    return np.array([sin(angle), -cos(angle)])


def translateMatrix(d):
    tMatrix = np.array([[1, 0, 0],
                        [0, 1, 0],
                        [d[0], d[1], 1]])
    return tMatrix


def rotateMatrix(theta, center: np.array):
    rMatrix = np.array([[cos(-theta), -sin(-theta), 0],
                        [sin(-theta),  cos(-theta), 0],
                        [0, 0, 1]])
    return translateMatrix(-1 * center).dot(rMatrix).dot(translateMatrix(center))


def scaleMatrix(s, center: np.array):
    sMatrix = np.array([[s[0], 0, 0],
                        [0, s[1], 0],
                        [0, 0, 1]])
    return translateMatrix(-1 * center).dot(sMatrix).dot(translateMatrix(center))


def objectNormalizationMatrix(window: np.array, windowRotation):
    tMatrix = translateMatrix(-1 * objectCenter(window))
    rMatrix = rotateMatrix(-windowRotation, np.array([0, 0]))
    centeredWindow = window.dot(tMatrix).dot(rMatrix)
    sMatrix = scaleMatrix([1 / centeredWindow[0, 0], 1 / centeredWindow[0, 1]], np.array([0, 0]))
    return tMatrix.dot(rMatrix).dot(sMatrix)


def transformViewPortX(Xw, Xwmin, Xwmax, Xvpmax, Xvpmin):
    return (Xw - Xwmin)/(Xwmax - Xwmin)*(Xvpmax - Xvpmin)


def transformViewPortY(Yw, Ywmin, Ywmax, Yvpmax, Yvpmin):
    return (1 - (Yw - Ywmin)/(Ywmax - Ywmin))*(Yvpmax - Yvpmin)