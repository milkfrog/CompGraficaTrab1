from math import *
import numpy as np

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
        return np.array([point[0],point[1],1])
  
    def homogenizePolygon(self,polygon):
        p = np.zeroes(shape(len(polygon),3))
        for i,point in enumerate(polygon):
            p[i] = self.homogenizePoint(polygon[i])
        return p

    def translate(self, homogenizedPolygon, tVector):
        tMatrix = np.array([[1,0,0],[0,1,0],[tVector[0],tVector[1],1]])
        return np.multiply(homogenizedPolygon, tMatrix)

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
            sumx += point[0]
            sumy += point[1]
        return self.homogenizePoint([sumx/n, sumy/n])