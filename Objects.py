from sympy import Matrix, symbols, summation
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
    def __init__(self, name, worldCoordinates, tipo, quantidade):
        self.name = name
        self.worldCoordinates = worldCoordinates
        self.windowCoordinates = worldCoordinates
        self.tipo = tipo
        self.quantidade = quantidade

    def center(self):
        i, j = symbols("i j", integer=True)
        objColumns = self.worldCoordinates.columnspace()
        sumx = summation(objColumns[0][i], (j, 0, i))
        sumy = summation(objColumns[1][i], (j, 0, i))
        n = len(self.worldCoordinates.rowspace())
        return Matrix([[sumx / n, sumy / n, 1]])

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

def translateMatrix(d):
    tMatrix = Matrix.eye(3)
    tMatrix[2, 0:1] = Matrix(d)
    return tMatrix


def rotateMatrix(theta, center):
    rMatrix = Matrix.eye(3)
    rMatrix[0:1, 0:1] = Matrix([cos(-theta), -sin(-theta)], [sin(-theta), cos(-theta)])
    return translateMatrix(-center) * rMatrix * translateMatrix(center)


def scaleMatrix(s, center):
    sMatrix = Matrix.eye(3)
    sMatrix[0:0, 1,1] = Matrix([s[0], 0], [0, s[1]])
    return translateMatrix(-center) * sMatrix * translateMatrix(center)


def normalizeMatrix(window: Objeto, windowRotation):
    tMatrix = translateMatrix(-window.center())
    rMatrix = rotateMatrix(-windowRotation, [0, 0])
    centeredWindow = window.worldCoordinates * tMatrix * rMatrix
    sMatrix = scaleMatrix([1 / centeredWindow[0, 0], 1 / centeredWindow[0, 1], 1], [0, 0, 1])
    return tMatrix * rMatrix * sMatrix


def transformViewPortX(Xw, Xwmin, Xwmax, Xvpmax, Xvpmin):
    return (Xw - Xwmin)/(Xwmax - Xwmin)*(Xvpmax - Xvpmin)


def transformViewPortY(Yw, Ywmin, Ywmax, Yvpmax, Yvpmin):
    return (1 - (Yw - Ywmin)/(Ywmax - Ywmin))*(Yvpmax - Yvpmin)


def liangBarskyClip(xmin, ymin, xmax, ymax, line):
    # Definicao de parametros
    p = Matrix([-(line[1,0] - line[0,0]), line[1,0] - line[0,0], -(line[1,1] - line[0,1]), line[1,1] - line[0,1]])
    q = Matrix([line[0,0] - xmin, xmax - line[0,0], line[0,1] - ymin, ymax - line[0,1]])
    posArr = Matrix.zeros(5)
    negArr = Matrix.zeros(5)
    posInd = 1
    negInd = 1

    # Certamente existe uma maneira mais Pythonica de escrever essa verificacao.
    if (p[0] == 0 and q[0] < 0) or (p[1] == 0 and q[1] < 0) or (p[2] == 0 and q[2] < 0) or (p[3] == 0 and q[3] < 0):
        return None # Linha paralela a clipping window

    if p[0] is not 0:
        r0 = q[0] / p[0]
        r1 = q[1] / p[1]
        if p[0] < 0:
            negArr[negInd] = r0
            posArr[posInd] = r1
        else:
            negArr[negInd] = r1
            posArr[posInd] = r0
        negInd += 1
        posInd += 1
    if p[2] is not 0:
        r2 = q[2] / p[2]
        r3 = q[3] / p[3]
        if p[2] < 0:
            negArr[negInd] = r2
            posArr[posInd] = r3
        else:
            negArr[negInd] = r3
            posArr[posInd] = r2
        negInd += 1
        posInd += 1

    rn0 = max(negArr)
    rn1 = min(posArr)

    if rn0 > rn1:
        return None # Linha fora da clipping window

    return Matrix([line[0,0] + p[1] * rn0, line[0,1] + p[3] * rn0], [line[0,0] + p[1] * rn1, line[0,1] + p[3] * rn1])