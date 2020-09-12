from math import *
import numpy as np

# A point is simply an array [x,y]
# A line is an array of 2 points [pointA,pointB]
# A polygon is an array of N points [[x1,y1],[x2,y2],[x3,y3] . . .]

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

  def viewPortTransform(self, point, Wmax, Wmin, VPmax, VPmin):
    x = (point[0] - Wmin[0]) / (Wmax[0] - Wmin[0]) * (VPmax[0] - VPmin[0])
    y = (1 - (point[1] - Wmin[1]))(Wmax[1] - Wmin[1]) * (VPmax[1] - VPmin[1])
    return self.homogenizePoint([x,y])
    
  def polygonCenter(self, polygon):
    n = len(polygon)
    sumx = 0
    sumy = 0
    for point in polygon:
      sumx += point[0]
      sumy += point[1]
    return self.homogenizePoint([sumx/n, sumy/n])