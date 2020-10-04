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
    def __init__(self, name, worldCoordinates: Matrix, tipo, quantidade):
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

def objectCenter(obj: Matrix):
    xColumns = obj[:,0]
    yColumns = obj[:,1]
    n = len(obj[:,0])
    x = sum(xColumns[i] for i in range(len(xColumns))) / n
    y = sum(yColumns[i] for i in range(len(yColumns))) / n
    return Matrix([[x, y]])


def viewUpVector(angle):
    return Matrix([[cos(angle), sin(angle)]])


def viewRightVector(angle):
    return Matrix([[sin(angle), -cos(angle)]])


def translateMatrix(d):
    tMatrix = Matrix.eye(3)
    try:
        tMatrix[2, 0:2] = d
    except:
        tMatrix[2, 0:2] = d.T
    return tMatrix


def rotateMatrix(theta, center):
    rMatrix = Matrix.eye(3)
    rMatrix[0:2, 0:2] = Matrix([[cos(-theta), -sin(-theta)], [sin(-theta), cos(-theta)]])
    return translateMatrix(-Matrix(center)) * rMatrix * translateMatrix(Matrix(center))


def scaleMatrix(s, center):
    sMatrix = Matrix.eye(3)
    sMatrix[0:2, 0:2] = Matrix([[s[0], 0], [0, s[1]]])
    return translateMatrix(-Matrix(center)) * sMatrix * translateMatrix(Matrix(center))


def objectNormalizationMatrix(window: Matrix, windowRotation):
    tMatrix = translateMatrix(-objectCenter(window))
    rMatrix = rotateMatrix(-windowRotation, [0, 0])
    centeredWindow = window * tMatrix * rMatrix
    sMatrix = scaleMatrix([1 / centeredWindow[0, 0], 1 / centeredWindow[0, 1], 1], [0, 0])
    return tMatrix * rMatrix * sMatrix


def transformViewPortX(Xw, Xwmin, Xwmax, Xvpmax, Xvpmin):
    return (Xw - Xwmin)/(Xwmax - Xwmin)*(Xvpmax - Xvpmin)


def transformViewPortY(Yw, Ywmin, Ywmax, Yvpmax, Yvpmin):
    return (1 - (Yw - Ywmin)/(Ywmax - Ywmin))*(Yvpmax - Yvpmin)


def liangBarskyClip(clpWndw, line):
    # A clpWndw deve ser 2 pontos (x,y) que formam a diagonal ascendente ( assim: / ) da window.
    # o primeiro ponto tem os valores x,y minimos e o segundo os maximos.
    # A line deve ser 2 pontos (x,y).

    # Definicao de parametros
    p = [-(line[1, 0] - line[0, 0]),
         line[0, 0] - line[1, 0],
         -(line[1, 1] - line[0, 1]),
         line[0, 1] - line[1, 1]]

    q = [line[0, 0] - clpWndw[0, 0],
         clpWndw[1, 0] - line[0, 0],
         line[0, 1] - clpWndw[0, 1],
         clpWndw[1, 1] - line[0, 1]]

    posArr = [0, 0, 0, 0, 0]
    posArr[0] = 1
    negArr = [0, 0, 0, 0, 0]
    negArr[0] = 0

    # Provavelmente existe uma maneira mais Pythonica de escrever essa verificacao.
    if (p[0] == 0 and q[0] < 0) or (p[1] == 0 and q[1] < 0) or (p[2] == 0 and q[2] < 0) or (p[3] == 0 and q[3] < 0):
        return None  # Linha paralela com a clipping window

    if p[0] is not 0:
        r0 = q[0] / p[0]
        r1 = q[1] / p[1]
        if p[0] < 0:
            negArr[1] = r0
            posArr[1] = r1
        else:
            negArr[1] = r1
            posArr[1] = r0

    if p[2] is not 0:
        r2 = q[2] / p[2]
        r3 = q[3] / p[3]
        if p[2] < 0:
            negArr[2] = r2
            posArr[2] = r3
        else:
            negArr[2] = r3
            posArr[2] = r2

    rn0 = max(negArr)
    rn1 = min(posArr)

    if rn0 > rn1:
        return None  # Linha fora da clipping window

    return Matrix([[line[0, 0] + p[1] * rn0, line[0, 1] + p[3] * rn0],
                   [line[0, 0] + p[1] * rn1, line[0, 1] + p[3] * rn1]])