from math import *
import sympy as sp

# A point is simply an array [x,y]
# A line is an array of 2 points [pointA,pointB]
# A polygon is an array of N points [[x1,y1],[x2,y2],[x3,y3] . . .]

class Coordenates:

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return str(self.x) + ',' + str(self.y)

class Objeto:
    def __init__(self, name, coordenates, tipo):
        self.name = name
        self.coordenates = coordenates
        self.tipo = tipo
    
    # TODO: deixar bonito o print pra aparecer na listagem direito
    # def __str__(self):
    #     stringCoordenadas = "["
    #     for i in coordenates:
    #         stringCoordenadas += 
    #     return self.name + "(" + self.tipo + ") coordenadas = " + 

class Operations:
    def homogenizePoint(self, point):
        return sp.matrix([[point[0],point[1],1]])

    def homogenizePolygon(self,polygon):
        pass

    def genericTransformation(self, object, tMatrix):
        temp_oMatrix = []
        for point in object.coordenates:
            temp_oMatrix.append([point.x, point.y, 1])
        oMatrix = sp.Matrix(temp_oMatrix)
        transformedMatrix = oMatrix * tMatrix
        coordinates = []
        for row in transformedMatrix.rowspace():
            coordinates.append(Coordenates(row[0],row[1]))
        return Objeto(object.name, coordinates, object.tipo)

    def translate(self, homogenizedPolygon, tVector):
        tMatrix = sp.Matrix([[1,0,0],[0,1,0],[tVector[0],tVector[1],1]])
        return homogenizedPolygon * tMatrix

    def scale(self, homogenizedPolygon, sVector):
        pass

    def rotate(self, homogenizedPolygon, center, theta):
        pass

    def transformViewPortX(self, Xw, Xwmin, Xwmax, Xvpmax, Xvpmin):
        return (Xw - Xwmin)/(Xwmax - Xwmin)*(Xvpmax - Xvpmin)
    
    def transformViewPortY(self, Yw, Ywmin, Ywmax, Yvpmax, Yvpmin):
        return (1 - (Yw - Ywmin)/(Ywmax - Ywmin))*(Yvpmax - Yvpmin)

    def polygonCenter(self, polygon):
        n = len(polygon)
        sumx = 0
        sumy = 0
        for point in polygon:
            sumx += point.x
            sumy += point.y
        return Coordenates(sumx/n, sumy/n)