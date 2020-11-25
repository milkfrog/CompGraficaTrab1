import numpy as np
from math import sin, cos, floor
from copy import deepcopy

class Coordenada:

    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def getList(self):
        return [self.x, self.y, self.z]


class Ponto:

    def __init__(self, nome, coordenadas, cor='#000000', normalizado=False):
        self.nome = nome
        self.coordenadas = coordenadas
        self.coordenadas.append(coordenadas[0])
        self.cor = cor
        self.normalizado = normalizado

        self.clipado = []
        self.centro = self.getCentro()

    def clipPonto(self):
        clipado = []
        if (abs(self.coordenadas[0].x) <= 1 and abs(self.coordenadas[0].y) <= 1):
            clipado.append(self.coordenadas)
        self.clipado = clipado

    def getCentro(self):
        return self.coordenadas
    

class Reta:
    
    def __init__(self, nome, coordenadas, cor='#000000', normalizado=False):
        self.nome = nome
        self.coordenadas = coordenadas
        self.cor = cor
        self.normalizado = normalizado

        self.clipado = []
        self.centro = self.getCentro()

    def getCentro(self):
        return Coordenada((self.coordenadas[0].x + self.coordenadas[1].x)/2, (self.coordenadas[0].y + self.coordenadas[1].y)/2)

    # Cohen-Sutherland
    def clipReta(self):
        clipado = []
        coordenadas = self.coordenadas
        listaRegionCodes = self.getRegionCodes(coordenadas)
        if (listaRegionCodes[0] == 0 and listaRegionCodes[1] == 0):
            clipado.append(coordenadas)
        elif (listaRegionCodes[0] & listaRegionCodes[1] != 0):
            pass
        elif (listaRegionCodes[0] & listaRegionCodes[1] == 0 and listaRegionCodes[0] != listaRegionCodes[1]):
            (novaCoordenada, regionCodeIntersecta) = self.getIntersecao(coordenadas[0], coordenadas[1], listaRegionCodes)
            if (regionCodeIntersecta):
                clipado.append(novaCoordenada)
        self.clipado = clipado

    def getRegionCodes(self, coordenadas):
        aux = []
        for i in coordenadas:
            code = int('0000', 2)
            if (i.x < -1):
                code = code | int('0001', 2)
            if (i.x > 1):
                code = code | int('0010', 2)
            if (i.y < -1):
                code = code | int('0100', 2)
            if (i.y > 1):
                code = code | int('1000', 2)
            aux.append(code)
        return aux

    def getIntersecao(self, ponto1, ponto2, listaRegionCodes):
        regionCodeIntersecta = False
        novaCoordenada = deepcopy([ponto1, ponto2])
        for i in range(2):
            regionCode = listaRegionCodes[i]
            # interseção em cima
            if (regionCode & int('1000', 2) == int('1000', 2)):
                m = (ponto2.x - ponto1.x) / (ponto2.y - ponto1.y)
                x = ponto1.x + m*(1 - ponto1.y)
                if (x >= -1 and x <= 1):
                    regionCodeIntersecta = True
                    novaCoordenada[i].x = x
                    novaCoordenada[i].y = 1
            # interseção em baixo
            if (regionCode & int('0100', 2) == int('0100', 2)):
                m = (ponto2.x - ponto1.x) / (ponto2.y - ponto1.y)
                x = ponto1.x + m*(-1 - ponto1.y)
                if (x >= -1 and x <= 1):
                    regionCodeIntersecta = True
                    novaCoordenada[i].x = x
                    novaCoordenada[i].y = -1
            # interseção a direita
            if (regionCode & int('0010', 2) == int('0010', 2)):
                m = (ponto2.y - ponto1.y) / (ponto2.x - ponto1.x)
                y = m*(1 - ponto1.x) + ponto1.y
                if (y >= -1 and y <= 1):
                    regionCodeIntersecta = True
                    novaCoordenada[i].x = 1
                    novaCoordenada[i].y = y
            # interseção a esquerda
            if (regionCode & int('0001', 2) == int('0001', 2)):
                m = (ponto2.y - ponto1.y) / (ponto2.x - ponto1.x)
                y = m*(-1 - ponto1.x) + ponto1.y
                if (y >= -1 and y <= 1):
                    regionCodeIntersecta = True
                    novaCoordenada[i].x = -1
                    novaCoordenada[i].y = y
        return (novaCoordenada, regionCodeIntersecta)
                

class Wireframe:
    
    def __init__(self, nome, coordenadas, tipoEspecifico='wireframe', cor='#000000', normalizado=False):
        self.nome = nome
        self.coordenadas = coordenadas
        self.cor = cor
        self.normalizado = normalizado
        self.tipoEspecifico = tipoEspecifico

        self.clipado = []
        self.centro = self.getCentro()

    def getCentro(self):
        x = 0
        y = 0
        for coordenada in self.coordenadas:
            x += coordenada.x
            y += coordenada.y
        return Coordenada((x/len(self.coordenadas)),(y/len(self.coordenadas)))

    def getIntersecao(self, ponto1, ponto2, listaRegionCodes):
        regionCodeIntersecta = False
        novaCoordenada = deepcopy([ponto1, ponto2])
        for i in range(2):
            regionCode = listaRegionCodes[i]
            # interseção em cima
            if (regionCode & int('1000', 2) == int('1000', 2)):
                m = (ponto2.x - ponto1.x) / (ponto2.y - ponto1.y)
                x = ponto1.x + m*(1 - ponto1.y)
                if (x >= -1 and x <= 1):
                    regionCodeIntersecta = True
                    novaCoordenada[i].x = x
                    novaCoordenada[i].y = 1
            # interseção em baixo
            if (regionCode & int('0100', 2) == int('0100', 2)):
                m = (ponto2.x - ponto1.x) / (ponto2.y - ponto1.y)
                x = ponto1.x + m*(-1 - ponto1.y)
                if (x >= -1 and x <= 1):
                    regionCodeIntersecta = True
                    novaCoordenada[i].x = x
                    novaCoordenada[i].y = -1
            # interseção a direita
            if (regionCode & int('0010', 2) == int('0010', 2)):
                m = (ponto2.y - ponto1.y) / (ponto2.x - ponto1.x)
                y = m*(1 - ponto1.x) + ponto1.y
                if (y >= -1 and y <= 1):
                    regionCodeIntersecta = True
                    novaCoordenada[i].x = 1
                    novaCoordenada[i].y = y
            # interseção a esquerda
            if (regionCode & int('0001', 2) == int('0001', 2)):
                m = (ponto2.y - ponto1.y) / (ponto2.x - ponto1.x)
                y = m*(-1 - ponto1.x) + ponto1.y
                if (y >= -1 and y <= 1):
                    regionCodeIntersecta = True
                    novaCoordenada[i].x = -1
                    novaCoordenada[i].y = y
        return (novaCoordenada, regionCodeIntersecta)

    def getRegionCodes(self, coordenadas):
        aux = []
        for i in coordenadas:
            code = int('0000', 2)
            if (i.x < -1):
                code = code | int('0001', 2)
            if (i.x > 1):
                code = code | int('0010', 2)
            if (i.y < -1):
                code = code | int('0100', 2)
            if (i.y > 1):
                code = code | int('1000', 2)
            aux.append(code)
        return aux

    def clipReta(self, pontos):
        listaRegionCodes = self.getRegionCodes(pontos)
        if (listaRegionCodes[0] == 0 and listaRegionCodes[1] == 0):
            return pontos
        elif (listaRegionCodes[0] & listaRegionCodes[1] != 0):
            return []
        elif (listaRegionCodes[0] & listaRegionCodes[1] == 0 and listaRegionCodes[0] != listaRegionCodes[1]):
            (novaCoordenada, regionCodeIntersecta) = self.getIntersecao(pontos[0], pontos[1], listaRegionCodes)
            if (regionCodeIntersecta):
                return novaCoordenada
            else:
                return []

    def bezier(self):
        aux = []
        mb = np.array([[-1,3,-3,1],[3,-6,3,0],[-3,3,0,0],[1,0,0,0]])
        for i in range(floor(len(self.coordenadas)/3)):
            p1 = self.coordenadas[3*i]
            p2 = self.coordenadas[3*(i+1)]
            p3 = self.coordenadas[3*(i+2)]
            p4 = self.coordenadas[3*(i+3)]
            gbX = np.array([[p1.x], [p2.x], [p3.x], [p4.x]])
            gbY = np.array([[p1.y], [p2.y], [p3.y], [p4.y]])
            for t in range(0, 1005, 5):
                aux1 = np.array([[pow(t/1000, 3), pow(t/1000, 2), t/1000, 1]])
                ptX = aux1.dot(mb).dot(gbX)
                ptY = aux1.dot(mb).dot(gbY)
                aux.append(Coordenada(ptX[0][0], ptY[0][0]))
        self.coordenadas = aux                

    def bSpline(self):
        aux = []
        mbs = np.array([[-1/6,1/2,-1/2,1/6],[1/2, -1, 1/2, 0],[-1/2, 0, 1/2, 0],[1/6, 4/6, 1/6, 0]])
        fator = 0.01
        aux1 = np.array([[0, 0, 0, 1], [pow(fator, 3), pow(fator, 2), fator, 0], [6*pow(fator, 3), 2*pow(fator, 2), 0, 0], [6*pow(fator, 3), 0, 0, 0]])
        fatorInverso = 1/fator
        for i in range(len(self.coordenadas) - 3):
            p1 = self.coordenadas[i]
            p2 = self.coordenadas[i+1]
            p3 = self.coordenadas[i+2]
            p4 = self.coordenadas[i+3]
            gbsX = np.array([[p1.x], [p2.x], [p3.x], [p4.x]])
            gbsY = np.array([[p1.y], [p2.y], [p3.y], [p4.y]])
            cX = mbs.dot(gbsX)
            cY = mbs.dot(gbsY)
            fsX = aux1.dot(cX)
            fsY = aux1.dot(cY)
            aux2 = self.forwardDifference(fatorInverso, fsX[0][0], fsX[1][0], fsX[2][0], fsX[3][0], fsY[0][0], fsY[1][0], fsY[2][0], fsY[3][0])
            aux += aux2
        self.coordenadas = aux

    def forwardDifference(self, fatorInverso, x, dx, d2x, d3x, y, dy, d2y, d3y):
        aux = []
        i = 1
        aux.append(Coordenada(x, y))
        while (i < fatorInverso):
            i += 1
            x += dx
            dx += d2x
            d2x += d3x
            y += dy
            dy += d2y
            d2y += d3y
            aux.append(Coordenada(x, y))
        return aux

    def clipCurvaEbSpline(self):
        i = 0
        aux = []
        while i < len(self.coordenadas) - 1:
            p1 = deepcopy(self.coordenadas[i])
            p2 = deepcopy(self.coordenadas[i + 1])
            novaCoordenada = self.clipReta([p1, p2])
            aux.append(novaCoordenada)
            i += 1
        self.clipado = aux

    def clipWireframe(self):
        i = 0
        wireframeCoordenadas = deepcopy(self.coordenadas)
        cima = [Coordenada(-1,1)]
        baixo = [Coordenada(1,-1)]
        direita = [Coordenada(1,1)]
        esquerda = [Coordenada(-1,-1)]
        entrantes = []
        window = []
        aux = []
        while i < len(wireframeCoordenadas):
            p1 = deepcopy(wireframeCoordenadas[i])
            p2 = deepcopy(wireframeCoordenadas[(i+1) % len(wireframeCoordenadas)])
            novaCoordenada = self.clipReta([p1,p2])
            for coordenada in novaCoordenada:
                entrou = False
                coordenada.flag = True
                if (novaCoordenada.index(coordenada) == 0 and not(abs(coordenada.x) <= 1 and abs(coordenada.y) <= 1) and coordenada not in entrantes):
                    entrantes.append(coordenada)
                    entrou = True
                if (coordenada not in wireframeCoordenadas):
                    wireframeCoordenadas.insert(i+1, coordenada)
                    i += 1
                elif (entrou):
                    wireframeCoordenadas[i+1].flag = True
                
                adicionado = False
                if (coordenada.y == 1):
                    for j in range(1, len(cima)):
                        if (coordenada.x == cima[j].x):
                            adicionado = True
                            break
                        if (coordenada.x < cima[j].x):
                            cima.insert(j, coordenada)
                            adicionado = True
                            break
                    if (not adicionado and abs(coordenada.x) != 1):
                        cima.append(coordenada)
                if (coordenada.y == -1):
                    for j in range(1, len(baixo)):
                        if (coordenada.x == baixo[j].x):
                            adicionado = True
                            break
                        if (coordenada.x > baixo[j].x):
                            baixo.insert(j, coordenada)
                            adicionado = True
                            break
                    if (not adicionado and abs(coordenada.x) != 1):
                        baixo.append(coordenada)
                if (coordenada.x == 1):
                    for j in range(1, len(direita)):
                        if (coordenada.y == direita[j].y):
                            adicionado = True
                            break
                        if (coordenada.y > direita[j].y):
                            direita.insert(j, coordenada)
                            adicionado = True
                            break
                    if (not adicionado and abs(coordenada.y) != 1):
                        direita.append(coordenada)
                if (coordenada.x == -1):
                    for j in range(1, len(esquerda)):
                        if (coordenada.y == esquerda[j].y):
                            adicionado = True
                            break
                        if (coordenada.y < esquerda[j].y):
                            esquerda.insert(j, coordenada)
                            adicionado = True
                            break
                    if (not adicionado and abs(coordenada.y) != 1):
                        esquerda.append(coordenada)
            i += 1
        window = cima + baixo + direita + esquerda

        if (len(entrantes) > 0):
            aux.append([])
            for ent in entrantes:
                if (ent in wireframeCoordenadas):
                    i = (wireframeCoordenadas.index(ent) + 1) % len(wireframeCoordenadas)
                    aux[-1].append(ent)
                    if (wireframeCoordenadas[i - 1].flag):
                        while not wireframeCoordenadas[i].flag:
                            if (abs(wireframeCoordenadas[i].x) <= 1 and abs(wireframeCoordenadas[i].y) <= 1):
                                aux[-1].append(wireframeCoordenadas[i])
                            i = (i+1) % len(wireframeCoordenadas)
                if (ent not in wireframeCoordenadas or wireframeCoordenadas[i] != ent):
                    aux2 = ent if ent not in wireframeCoordenadas else wireframeCoordenadas[i]
                    aux[-1].append(aux2)
                    i = (window.index(aux2)+1) % len(window)
                    while not window[i].flag:
                        aux[-1].append(window[i])
                        i = (i+1) % len(window)
                    aux[-1].append(window[i])
                    if (window[i] == ent):
                        aux.append([])
            self.clipado = aux
        else:
            self.clipado = [list(filter(lambda var: (abs(var.x) <= 1 and abs(var.y) <= 1), wireframeCoordenadas))]
