import numpy as np

from itertools import cycle

from drawable import Drawable

import dot
import line

class Wireframe(Drawable):
    def __init__(self, dot_list, color_list=cycle([(0,0,0)]),w_size=(500,500), offset=(10,10)):
        self.scale = np.array([[w_size[0], 0, 0, 0],
                               [0, w_size[1], 0, 0],
                               [0, 0, w_size[1], 0],
                               [0, 0, 0, 1]
                              ])
        coords = np.array(list(map(dot.Dot.coordenates,dot_list)))
        self.n_coords = coords@np.array([[1/w_size[0], 0, 0, 0],
                                              [0, 1/w_size[1], 0, 0],
                                              [0, 0, 1/w_size[1], 0],
                                              [0, 0, 0, 1]
                                           ])
        self.off = np.array([[1, 0, 0, 0],
                                              [0, 1, 0, 0],
                                              [0, 0, 1, 0],
                                              [260, 260, 260, 1]
                                           ])
        self.color_list = color_list
        self.w_size = w_size
        self.bounds = w_size[0]+offset[0], w_size[1]+offset[1]
        self.bx, self.by = self.bounds
        self.offset = offset

    def coordenates(self):
        return self.n_coords@self.scale

    def normal_coordenates(self):
        return self.n_coords
    
    def draw_persp(self, cr, matrix, offset): # passar a matriz com 1/d mtxd@coords@mtx
        d = 260
        temp_ = self.coordenates()@matrix + (0,0,d,0)#@self.off
        for i,j in enumerate(temp_):
            zd = j[2]/d
            temp_[i][0] = temp_[i][0]/zd
            temp_[i][1] = temp_[i][1]/zd
            temp_[i][2] = d
        
        temp_ = temp_ + (260,260,0,0)#@self.off

        for p1, p2, color in zip(temp_, temp_[1:], self.color_list):
            drw, cps = self.clipSC(np.array([p1,p2]))
            p1c, p2c = cps
            if drw:
                continue    
            cr.move_to(p1c[0], p1c[1])
            cr.line_to(p2c[0], p2c[1])
            cr.set_source_rgb(color[0], color[1], color[2])
            cr.stroke()
    
    def draw(self, cr, matrix, offset):
        temp_ = self.coordenates()@matrix + (260,260,260,0)#@self.off
        for p1, p2, color in zip(temp_, temp_[1:], self.color_list):
            drw, cps = self.clipSC(np.array([p1,p2]))
            p1c, p2c = cps
            if drw:
                continue    
            cr.move_to(p1c[0], p1c[1])
            cr.line_to(p2c[0], p2c[1])
            cr.set_source_rgb(color[0], color[1], color[2])
            cr.stroke()

    def transform(self, matrix):
        self.n_coords = self.n_coords@matrix

    def transcript(self):
        points = ""
        for p in self.coordenates():
            points = "v {} {} {}".format(p[0],p[1],p[2]) if not points else '\n'.join([points, "v {} {} {}".format(p[0],p[1],p[2])])

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
