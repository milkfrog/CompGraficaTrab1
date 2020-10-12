import numpy as np

from math import pi

from drawable import Drawable

class Dot(Drawable):
    def __init__(self, x, y, z, color=(0,0,0), w_size=(500,500), offset=(10,10)):
        self.scale = np.array([[w_size[0], 0, 0, 0],
                               [0, w_size[1], 0, 0],
                               [0, 0, w_size[1], 0],
                               [0, 0, 0, 1],
                              ])
        coords = np.array([float(x), float(y), float(z), 1])
        self.n_coords = coords@np.array([[1/w_size[0], 0, 0,0],
                                              [0, 1/w_size[1], 0,0],
                                              [0, 0, 1/w_size[1],0],
                                              [0, 0, 0, 1],
                                           ])

        self.r, self.g, self.b = color
        self.w_size = w_size
        self.bounds = w_size[0]+offset[0], w_size[1]+offset[1]
        self.offset = offset

    def coordenates(self):
        return self.n_coords@self.scale
    
    def normal_coordenates(self):
        return self.n_coords
    
    def draw_persp(self, cr, matrix, offset):#, matrix_tr):
        d = 260
        temp_ = self.coordenates()@matrix + (0,0,260,0)# + offset
        zd = temp_[2]/d
        temp_[0] = temp_[0]/zd
        temp_[1] = temp_[1]/zd
        temp_[2] = d
        temp_[3] = 1
        temp_ = temp_ + (260,260,0,0)# + offset
        temp_ = self.clip(temp_)# + offset
        if temp_[0] <= self.offset[0] or temp_[0] >= self.bounds[0] or temp_[1] <= self.offset[1] or temp_[1] >= self.bounds[1]:
            return
        cr.move_to(temp_[0], temp_[1])
        cr.arc(temp_[0], temp_[1], 4, 0, 2*pi)
        cr.set_source_rgb(self.r, self.g, self.b)
        cr.fill()

    def draw(self, cr, matrix, offset):#, matrix_tr):
        temp_ = self.clip(self.coordenates()@matrix + (260,260,260,0))# + offset
        if temp_[0] <= self.offset[0] or temp_[0] >= self.bounds[0] or temp_[1] <= self.offset[1] or temp_[1] >= self.bounds[1]:
            return
        cr.move_to(temp_[0], temp_[1])
        cr.arc(temp_[0], temp_[1], 4, 0, 2*pi)
        cr.set_source_rgb(self.r, self.g, self.b)
        cr.fill()

    def transform(self, matrix):
        self.n_coords = self.n_coords@matrix

    def transcript(self):
        c_aux = self.coordenates()
        return "p","v {} {} {}".format(c_aux[0], c_aux[1], c_aux[2])

    def clip(self, mtx):
        tmp_ = []
        mm = lambda x: (min(max(self.offset[0],x[0]),self.bounds[0]), min(max(self.offset[1],x[1]),self.bounds[1]), 1)
        return mm(mtx)
