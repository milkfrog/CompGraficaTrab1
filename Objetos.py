import numpy as np
from math import sin, cos
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
    
    def __init__(self, nome, coordenadas, cor='#000000', normalizado=False, tipoEspecifico='wireframe'):
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
