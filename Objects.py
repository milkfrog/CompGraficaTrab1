import sympy as sp

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
    def __init__(self, name, coordinates, tipo, quantidade):
        self.quantidade = quantidade
        self.name = name
        self.coordinates = coordinates
        self.tipo = tipo
    
    # TODO: deixar bonito o print pra aparecer na listagem direito
    # def __str__(self):
    #     stringCoordenadas = "["
    #     for i in coordenates:
    #         stringCoordenadas += 
    #     return self.name + "(" + self.tipo + ") coordenadas = " + 


def homogenizePoint(point):
    return sp.Matrix([[point[0], point[1], 1]])


def genericTransformation(obj, tMatrix):
    temp_oMatrix = []
    for point in obj.coordinates:
        temp_oMatrix.append([point.x, point.y, point.z])
    oMatrix = sp.Matrix(temp_oMatrix)
    transformedMatrix = oMatrix * tMatrix
    coordinates = []
    for i in range(obj.quantidade):
        coordinates.append(Coordinates(transformedMatrix.row(i)[0], transformedMatrix.row(i)[1]))
    return Objeto(obj.name, coordinates, obj.tipo, obj.quantidade)


def transformViewPortX(Xw, Xwmin, Xwmax, Xvpmax, Xvpmin):
    return (Xw - Xwmin)/(Xwmax - Xwmin)*(Xvpmax - Xvpmin)


def transformViewPortY(Yw, Ywmin, Ywmax, Yvpmax, Yvpmin):
    return (1 - (Yw - Ywmin)/(Ywmax - Ywmin))*(Yvpmax - Yvpmin)


def polygonCenter(polygon):
    n = len(polygon)
    sumx = 0
    sumy = 0
    for point in polygon:
        sumx += point.x
        sumy += point.y
    return Coordinates(sumx/n, sumy/n)