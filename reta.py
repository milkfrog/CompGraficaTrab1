import numpy as np

import Objects as Operations
import ponto

class Reta():
    def __init__(self, ponto1: ponto, ponto2: ponto, wSize, normalizationMatrix = np.eye(4, 4), offset=(10,10), color=(0,0,0)):

        self.worldCoordinates = np.array([ponto1.worldCoordinates, ponto2.worldCoordinates])

        self.wSize = wSize

        self.normalizationMatrix = normalizationMatrix

        self.r, self.g, self.b = color
        self.bounds = wSize[0] + offset[0], wSize[1] + offset[1]
        self.offset = offset
        self.clip = self.clipSC

    def normalizedCoordinates(self):
        return self.worldCoordinates @ self.normalizationMatrix

    def viewPortCoordinates(self):
        return Operations.transformViewPort(self.normalizedCoordinates(), self.wSize)
    
    def draw_persp(self, cr, matrix, offset): # passar a matriz com 1/d mtxd@coords@mtx
        d = 260
        temp_ = self.worldCoordinates @ matrix + (0,0,d,0)#@self.off
        for i,j in enumerate(temp_):
            zd = j[2]/d
            temp_[i][0] = temp_[i][0]/zd
            temp_[i][1] = temp_[i][1]/zd
            temp_[i][2] = d
        
        temp_ = temp_ + (260,260,0,0)#@self.off

        for p1, p2 in zip(temp_, temp_[1:]):
            drw, cps = self.clipSC(np.array([p1,p2]))
            p1c, p2c = cps
            if drw:
                continue    
            cr.move_to(p1c[0], p1c[1])
            cr.line_to(p2c[0], p2c[1])
            cr.set_source_rgb(self.r, self.g, self.b)
            cr.stroke()
    #def draw_persp(self, cr, matrix, offset):#, matrix_tr):
    #    drw, temp_ = self.clip(self.worldCoordinates()@matrix + (260,260,260,0))# + offset
    #    if drw:
    #        return
    #    cr.move_to(temp_[0][0], temp_[0][1])
    #    cr.line_to(temp_[1][0], temp_[1][1])
    #    cr.set_source_rgb(self.r, self.g, self.b)
    #    cr.stroke()
    def draw(self, cr, matrix, offset):#, matrix_tr):
        drw, temp_ = self.clip(self.worldCoordinates @ matrix + (260,260,260,0))# + offset
        if drw:
            return
        cr.move_to(temp_[0][0], temp_[0][1])
        cr.line_to(temp_[1][0], temp_[1][1])
        cr.set_source_rgb(self.r, self.g, self.b)
        cr.stroke()

    def transform(self, matrix):
        self.n_coords = self.n_coords.dot(matrix)

    def transcript(self):
        points = ""
        for p in self.worldCoordinates:
            points = "v {} {} {}".format(p[0],p[1], p[2]) if not points else '\n'.join([points,"v {} {} {}".format(p[0],p[1], p[2])])

        return "l",points

    def clipSC(self, mtx): 
        RC_l = lambda x: (x[1] < self.offset[1], x[1] > self.bounds[1],  
                         x[0] > self.bounds[1], x[0] < self.offset[0])
        t = mtx
        RC = []
        mm = lambda x: (min(max(self.offset[0],x[0]),self.bounds[0]), min(max(self.offset[1],x[1]),self.bounds[1]), 1)
        for d in mtx:
            RC.append(RC_l(d))

        x1,x2,y1,y2 = mtx[0][0], mtx[1][0], mtx[0][1], mtx[1][1]
        RC_t = [x and y for x,y in zip(RC[0],RC[1])]

        RC_s = 0

        for i, d in enumerate(mtx):
            if x2==x1:
                x_int, y_int, _ = mm(t[i])
                t[i][0] = x_int
                t[i][1] = y_int
                continue
            
            m = (y2-y1)/(x2-x1)
            y_int, x_int = t[i][1], t[i][0]
            if RC[i][0]:
                x_int = (1/m)*(self.offset[1] - t[i][1]) + t[i][0] if m else self.bounds[1] # M != 0
                y_aux = self.offset[1] 

            if RC[i][1]:
                x_int = (1/m)*(self.bounds[1]- t[i][1]) + t[i][0] if m else self.offset[1] # M != 0
                y_aux = self.bounds[1] 

            if RC[i][2]:
                y_int = m*(self.bounds[0] - t[i][0]) + t[i][1] 
                x_aux = self.bounds[0] 

            if RC[i][3]:
                y_int = m*(self.offset[0]-t[i][0]) + t[i][1]
                x_aux = self.offset[0] 
            try:
                t[i][1] = y_int if y_int <= self.bounds[1] and y_int >= self.offset[1] else y_aux
                t[i][0] = x_int if x_int <= self.bounds[0] and x_int >= self.offset[0] else x_aux
            except Exception as err:
                RC_s = 1
            
        RC_s += sum(RC_t)

        return RC_s, t
