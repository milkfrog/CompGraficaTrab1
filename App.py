# coding: utf-8
from tkinter import *
from tkinter import ttk
import numpy as np
from math import sin, cos, pi, ceil, sqrt, atan
from copy import deepcopy

from Objetos import *


class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("Trabalho 1 de Computação Gráfica INE5420")
        # limitando o tamanho do App em 1200x800
        self.root.minsize(1200, 800)
        self.root.maxsize(1200, 800)

        # render frame do Widget:
        self.renderWidget()

        # Configs iniciais:
        self.displayFile = []
        self.displayFileNormalizado = []
        self.displayFileClipado = []

        # config da Window:
        self.window = np.array([[0,0,0],[0,self.canvas.winfo_height(),0],[self.canvas.winfo_width(),self.canvas.winfo_height(),0],[self.canvas.winfo_width(),0,0]])
        (x,y,z) = (0,0,0)
        for i in self.window:
            x += i[0]
            y += i[1]
            z += i[2]
        self.windowCenter = [x/len(self.window), y/len(self.window), z/len(self.window)]
        self.windowNormal = [Coordenada(-1,-1), Coordenada(1,-1), Coordenada(1,1), Coordenada(-1,1)]

        # config da ViewPort:
        self.padViewPort = 20
        self.viewPort = [Coordenada(0+self.padViewPort,0+self.padViewPort),Coordenada(0+self.padViewPort,self.canvas.winfo_height()-self.padViewPort),Coordenada(self.canvas.winfo_width()-self.padViewPort,self.canvas.winfo_height()-self.padViewPort),Coordenada(self.canvas.winfo_width()-self.padViewPort,0+self.padViewPort)]

        self.anguloRotacaoWindowEixoX = 0
        self.anguloRotacaoWindowEixoY = 0
        self.anguloRotacaoWindowEixoZ = 0
       

        # Inicializa:
        self.renderObjetcs()
        self.root.mainloop()

    def renderWidget(self):
        # frame do Menu de Funções:
        menuDeFuncoes = LabelFrame(self.root, text="Menu de Funções", width=100)
        menuDeFuncoes.pack(side=LEFT, fill=Y)

        # frame dos objetos:
        frameObjetos = Frame(menuDeFuncoes)
        frameObjetos.pack()
        labelObjetos = Label(frameObjetos, text="Objetos")
        labelObjetos.pack()
        self.listObjects = Listbox(frameObjetos, width=40, selectmode=SINGLE)
        self.listObjects.pack()
        frameRemoveAdd = Frame(frameObjetos)
        frameRemoveAdd.pack(pady=(10, 0))
        Button(frameRemoveAdd, text="Incluir Objeto", bg="lightgreen", command=self.addObject).pack(side=LEFT, padx=(5, 15))
        Button(frameRemoveAdd, text="Remover Objeto", bg="#ffcccb", command=self.removeObject).pack(side=RIGHT, padx=(0, 5))
        
        # frame da Window:
        labelWindow = LabelFrame(menuDeFuncoes, text="Window", width=100)
        labelWindow.pack(side=TOP, fill=X, pady=(10,0))
        frameDirecoes = Frame(labelWindow)
        frameDirecoes.pack(side=LEFT, fill=X)
        frameZoom = Frame(labelWindow)
        frameZoom.pack(side=RIGHT)
        Button(frameDirecoes, text="↑", command=lambda: self.moveWindow("↑")).grid(row=0, column=1)
        Button(frameDirecoes, text="←", command=lambda: self.moveWindow("←")).grid(row=1, column=0)
        Button(frameDirecoes, text="↓", command=lambda: self.moveWindow("↓")).grid(row=1, column=1)
        Button(frameDirecoes, text="→", command=lambda: self.moveWindow("→")).grid(row=1, column=2)
        Button(frameZoom, text="+", command=lambda: self.zoomWindow("+")).grid(row=0, column=0)
        Button(frameZoom, text="-", command=lambda: self.zoomWindow("-")).grid(row=1, column=0)
        frameRotacao = Frame(labelWindow)
        frameRotacao.pack()
        Label(frameRotacao, text="Eixo X: ").grid(row=0, column=0)
        Button(frameRotacao, text="↻", command=lambda: self.rotateWindow("↻", "x")).grid(row=0, column=1)
        Button(frameRotacao, text="↺", command=lambda: self.rotateWindow("↺", "x")).grid(row=0, column=2)
        Label(frameRotacao, text="Eixo Y: ").grid(row=1, column=0)
        Button(frameRotacao, text="↻", command=lambda: self.rotateWindow("↻", "y")).grid(row=1, column=1)
        Button(frameRotacao, text="↺", command=lambda: self.rotateWindow("↺", "y")).grid(row=1, column=2)
        Label(frameRotacao, text="Eixo Z: ").grid(row=2, column=0)
        Button(frameRotacao, text="↻", command=lambda: self.rotateWindow("↻", "z")).grid(row=2, column=1)
        Button(frameRotacao, text="↺", command=lambda: self.rotateWindow("↺", "z")).grid(row=2, column=2)
        

        # frame de Transformacao de Objetos
        self.opcaoCentroDeRotacao = StringVar()
        opcoesCentroDeRotacao = {'Mundo', 'Objeto', 'Ponto Qualquer'}
        self.opcaoCentroDeRotacao.set('Objeto')
        self.centroDeRotacaoX = DoubleVar()
        self.centroDeRotacaoY = DoubleVar()
        labelTransformacoes = LabelFrame(menuDeFuncoes, text="Trasformacao de Objetos", width=100)
        labelTransformacoes.pack(side=TOP, fill=X, pady=(10, 0))
        labelTranslacaoEscalonamento = LabelFrame(labelTransformacoes, text="Translacao e Escalonamento")
        labelTranslacaoEscalonamento.pack(side=TOP, fill=X)
        frameTranslacao = Frame(labelTranslacaoEscalonamento)
        frameTranslacao.pack(side=LEFT, fill=X)
        frameEscalonamento = Frame(labelTranslacaoEscalonamento)
        frameEscalonamento.pack(side=RIGHT)
        labelRotacao = LabelFrame(labelTransformacoes, text="Rotacao")
        labelRotacao.pack(side=TOP, fill=X)
        frameRotacaoBotoes = Frame(labelRotacao)
        frameRotacaoBotoes.pack(side=LEFT, fill=X)
        frameRotacaoOpcoes = Frame(labelRotacao)
        frameRotacaoOpcoes.pack(side=RIGHT)
        Button(frameTranslacao, text="↑", command=lambda: self.moveObject("↑")).grid(row=0, column=1)
        Button(frameTranslacao, text="←", command=lambda: self.moveObject("←")).grid(row=1, column=0)
        Button(frameTranslacao, text="↓", command=lambda: self.moveObject("↓")).grid(row=1, column=1)
        Button(frameTranslacao, text="→", command=lambda: self.moveObject("→")).grid(row=1, column=2)
        Button(frameEscalonamento, text="+", command=lambda: self.scaleObject("+")).grid(row=0, column=0)
        Button(frameEscalonamento, text="-", command=lambda: self.scaleObject("-")).grid(row=1, column=0)
        Button(frameRotacaoBotoes, text="↺", command=lambda: self.rotateObject("l")).grid(row=0, column=0)
        Button(frameRotacaoBotoes, text="↻", command=lambda: self.rotateObject("r")).grid(row=0, column=1)
        Label(frameRotacaoOpcoes, text="Centro: ").grid(row=0, column=0)
        OptionMenu(frameRotacaoOpcoes, self.opcaoCentroDeRotacao, *opcoesCentroDeRotacao).grid(row=0, column=1)
        Label(frameRotacaoOpcoes, text="X = ").grid(row=1, column=0)
        Entry(frameRotacaoOpcoes, textvariable=self.centroDeRotacaoX, width=10).grid(row=1,column=1)
        Label(frameRotacaoOpcoes, text="Y = ").grid(row=2, column=0)
        Entry(frameRotacaoOpcoes, textvariable=self.centroDeRotacaoY, width=10).grid(row=2, column=1)

        # frame da ViewPort:
        frameViewPort = LabelFrame(self.root, text="ViewPort")
        frameViewPort.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(frameViewPort, bg="#fff", width=850, height=650)
        self.canvas.grid(row=0, column=0)

        # frame de Log:
        frameLog = LabelFrame(frameViewPort, text="Log")
        frameLog.grid(row=1, column=0)
        # height e width do Listbox NÃO é em pixel, e sim em chars
        self.log = Listbox(frameLog, height=5, width=106)
        self.log.pack(fill=X)

        self.root.update_idletasks()
        print("Canvas w: " + str(self.canvas.winfo_width()) + ", and h: " + str(self.canvas.winfo_height()))

    def renderObjetcs(self):
        # deletando o que tiver desenhado no canvas:
        self.canvas.delete("all")
        self.root.update_idletasks()

        # inclui linha vermelha da viewport:
        coordenadasViewPort = []
        for ponto in self.viewPort:
            coordenadasViewPort += [ponto.x, ponto.y]
        self.canvas.create_polygon(coordenadasViewPort, outline='#ff0000', fill="")

        self.getDisplayFileNormalizado()
        self.cliparObjetos()

        # inicio desenho no canvas:
        for o in self.displayFileClipado:
            for coordenadas in o.clipado:   
                coordenadasCanvas = []
                for coordenada in coordenadas:
                    coordenadasCanvas += [coordenada.x + self.padViewPort, coordenada.y + self.padViewPort]
                if isinstance(o, Ponto):
                    self.canvas.create_oval(coordenadasCanvas[0] - 0.5 + self.padViewPort, coordenadasCanvas[1] - 0.5 +self.padViewPort, coordenadasCanvas[0] + 0.5 + self.padViewPort, coordenadasCanvas[1] + 0.5 + self.padViewPort, fil=o.cor)
                if isinstance(o, Reta):
                    self.canvas.create_line(coordenadasCanvas, fill=o.cor)
                if isinstance(o, Wireframe):
                    self.canvas.create_polygon(coordenadasCanvas, outline=o.cor, fill="")

    def cliparObjetos(self):
        self.displayFileClipado = []
        for objetoNormalizado in self.displayFileNormalizado:
            aux = deepcopy(objetoNormalizado)
            if isinstance(aux, Ponto):
                aux.clipPonto()
            if isinstance(aux, Reta):
                aux.clipReta()
            if (isinstance(aux, Wireframe) and aux.tipoEspecifico == 'wireframe'):
                aux.clipWireframe()
            if (isinstance(aux, Wireframe) and aux.tipoEspecifico == 'curva'):
                pass
            if (isinstance(aux, Wireframe) and aux.tipoEspecifico == 'bSpline'):
                pass
            clipAux = []
            for coord in aux.clipado:
                if (len(coord) == 1):
                    clipAux.append(coord)
                    continue
                arestaAux = deepcopy(coord)
                for i in [0,1]:
                    if (not isinstance(coord[i], Coordenada)):
                        arestaAux[i] = aux.coordenadas[coord[i]]
                clipAux.append(arestaAux)
            aux.clipado = list(map(self.transformaCoordenadas, clipAux))
            self.displayFileClipado.append(aux)

    def transformaCoordenadas(self, coordenadas):
        aux = []
        for coordenada in coordenadas:
            aux.append(self.getViewportCoordenadas(coordenada))
        return aux

    def getViewportCoordenadas(self, coordenadas):
        vpCoordMin = self.viewPort[0]
        vpCoordMax = self.viewPort[2]
        wCoordMin = self.windowNormal[0]
        wCoordMax = self.windowNormal[2]
        x = (coordenadas.x - wCoordMin.x)*(vpCoordMax.x - vpCoordMin.x)/(wCoordMax.x - wCoordMin.x)
        y = (1 - ((coordenadas.y - wCoordMin.y)/(wCoordMax.y - wCoordMin.y)))*(vpCoordMax.y - vpCoordMin.y)
        return Coordenada(x,y)

    def getDisplayFileNormalizado(self):
        self.displayFileNormalizado = []
        matrizSCN = self.getMatrizSCN().tolist()
        objetos = deepcopy(self.displayFile)
        
        # incluir config na GUI pra deicidir entre qual projecao:
        # self.projecaoPerspectiva(objetos)
        # self.projecaoParalela()  

        for objeto in objetos:
            aux = []
            for coordenada in objeto.coordenadas:
                coord = np.array([[coordenada.x, coordenada.y, coordenada.z, 1]]).dot(np.array(matrizSCN)).tolist()
                aux.append(Coordenada(coord[0][0], coord[0][1], coord[0][2]))
            objeto.normalizado = True
            objeto.coordenadas = aux
            self.displayFileNormalizado.append(objeto)

    def projecaoParalela(self):
        aux1 = np.array([[self.windowCenter[0], self.windowCenter[1], self.windowCenter[2], 1]])
        windowCenterNegativo = np.array(self.windowCenter).dot(-1)
        aux2 = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[windowCenterNegativo[0], windowCenterNegativo[1], windowCenterNegativo[2], 1]]
        vrpt = np.delete(aux1.dot(aux2), 3, 1)
        p1 = vrpt - np.array(self.window[0]) - np.array(self.windowCenter)
        p2 = np.array(self.window[1]) - np.array(self.windowCenter) - vrpt
        vpn = np.array([p1[0][1] * p2[0][2] - p1[0][2] * p2[0][1], p1[0][2] * p2[0][0] - p1[0][0] * p2[0][2], p1[0][0] * p2[0][1] - p1[0][1] * p2[0][0]])
        valor1 = 0 if vpn[2] == 0 else vpn[1]/vpn[2]
        valor2 = 0 if vpn[2] == 0 else vpn[0]/vpn[2]
        teta = [atan(valor1), atan(valor2)]
        aux3 = []
        for coordenada in self.window:
            aux3.append(np.delete(np.array([coordenada[0],coordenada[1],coordenada[2],1]).dot(np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[-self.windowCenter[0],-self.windowCenter[1],-self.windowCenter[2],1]])),3,0).tolist())
        tetaX = round((360-teta[0])*(pi/180), 5)
        tetaY = round((360-teta[1])*(pi/180), 5)
        rotacaoX = np.array([[1,0,0,0],[0,round(cos(tetaX),5),round(sin(tetaX),5),0],[0,round(-sin(tetaX),5),round(cos(tetaX),5),0],[0,0,0,1]])
        rotacaoY = np.array([[round(cos(tetaY),5),0,round(-sin(tetaY),5),0],[0,1,0,0],[round(sin(tetaY),5),0,round(cos(tetaY),5),0],[0,0,0,1]])
        aux4 = []
        for coordenada in aux3:
            aux4.append(np.delete(np.array([[coordenada[0],coordenada[1],coordenada[2],1]]).dot(rotacaoX).dot(rotacaoY),3,1)[0].tolist())
        self.window = np.array(aux4)
        for objeto in self.displayFile:
            aux5 = []
            for coordenada in objeto.coordenadas:
                coord = np.delete(np.array([coordenada.x,coordenada.y,coordenada.z,1]).dot(np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[-self.windowCenter[0],-self.windowCenter[1],-self.windowCenter[2],1]])),3,0).tolist()
                aux5.append(Coordenada(coord[0], coord[1], coord[2]))
            aux6 = []
            for coordenada in aux5:
                coord = np.delete(np.array([[coordenada.x,coordenada.y,coordenada.z,1]]).dot(rotacaoX).dot(rotacaoY),3,1)[0].tolist()
                aux6.append(Coordenada(coord[0], coord[1], coord[2]))
            objeto.coordenadas = aux6
            if (isinstance(objeto, Wireframe) and objeto.tipoEspecifico == 'Curva'):
                objeto.arestas = []
                for i in range(len(objeto.coordenadas)-1):
                    objeto.arestas.append([i, i+1])

    def projecaoPerspectiva(self):
        pass

    def getMatrizSCN(self):
        matrizDeTranslacao = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[-self.windowCenter[0],-self.windowCenter[1],-self.windowCenter[2],1]])
        (anguloX, anguloY, anguloZ) = (360-self.anguloRotacaoWindowEixoX)*(pi/180), (360-self.anguloRotacaoWindowEixoY)*(pi/180), (360-self.anguloRotacaoWindowEixoZ)*(pi/180)
        matrizDeRotacao = np.array([[1,0,0,0],[0,round(cos(anguloX),5),round(sin(anguloX),5),0],[0,round(-sin(anguloX),5),round(cos(anguloX),5),0],[0,0,0,1]]).dot(np.array([[round(cos(anguloY),5),0,round(-sin(anguloY),5),0],[0,1,0,0],[round(sin(anguloY),5),0,round(cos(anguloY),5),0],[0,0,0,1]])).dot(np.array([[round(cos(anguloZ),5),round(sin(anguloZ),5),0,0],[round(-sin(anguloZ),5),round(cos(anguloZ),5),0,0],[0,0,1,0],[0,0,0,1]]))
        windowWidth = sqrt((self.window[1][0]-self.window[0][0])**2 + (self.window[1][1]-self.window[0][1])**2)/2
        windowHeight = sqrt((self.window[3][0]-self.window[0][0])**2 + (self.window[3][1]-self.window[0][1])**2)/2
        matrizDeEscala = np.array([[1/windowWidth,0,0,0],[0,1/windowHeight,0,0],[0,0,1,0],[0,0,0,1]])
        return matrizDeTranslacao.dot(matrizDeRotacao).dot(matrizDeEscala)

    def zoomWindow(self, tipo):
        zoomValue = 0.1
        if tipo == "+":
            valor = 1 - zoomValue
        if tipo == "-":
            valor = 1 + zoomValue
        centro = self.windowCenter
        matriz1 = []
        for coordenada in self.window:
            aux1 = np.array([[coordenada[0],coordenada[1],coordenada[2],1]])
            aux2 = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[-centro[0],-centro[1],-centro[2],1]])
            final = aux1.dot(aux2).tolist()
            matriz1.append(final[0])
        self.window = matriz1
        matriz2 = []
        for coordenada in self.window:
            aux3 = np.array([[coordenada[0],coordenada[1],coordenada[2],1]])
            aux4 = np.array([[valor, 0,0,0],[0,valor,0,0],[0,0,1,0],[0,0,0,1]])
            final2 = aux3.dot(aux4).tolist()
            matriz2.append(final2[0])
        self.window = matriz2
        matriz3 = []
        for coordenada in self.window:
            aux1 = np.array([[coordenada[0],coordenada[1],coordenada[2],1]])
            aux2 = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[centro[0],centro[1],centro[2],1]])
            final = aux1.dot(aux2).tolist()
            matriz3.append(final[0])
        self.window = matriz3
        # atualiza centro:
        (x,y,z) = (0,0,0)
        for i in self.window:
            x += i[0]
            y += i[1]
            z += i[2]
        self.windowCenter = [x/len(self.window), y/len(self.window), z/len(self.window)]
        self.log.insert(0, "zoom "+tipo+" na Window")
        self.renderObjetcs()

    def moveWindow(self, direction):
        valor = 0.1
        Cx = 0
        Cy = 0
        windowWidth = sqrt((self.window[1][0]-self.window[0][0])**2 + (self.window[1][1]-self.window[0][1])**2)/2
        windowHeight = sqrt((self.window[3][0]-self.window[0][0])**2 + (self.window[3][1]-self.window[0][1])**2)/2
        if direction == "↑":
            Cy = windowHeight * valor
        elif direction == "←":
            Cx = -windowWidth * valor
        elif direction == "↓":
            Cy = -windowHeight * valor
        elif direction == "→":
            Cx = windowWidth * valor
        aux = []
        for coordenada in self.window:
            aux1 = np.array([[coordenada[0],coordenada[1],coordenada[2],1]])
            aux2 = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[Cx,Cy,0,1]])
            final = aux1.dot(aux2).tolist()
            aux.append(final[0])
        self.window = aux
        (x,y,z) = (0,0,0)
        for i in self.window:
            x += i[0]
            y += i[1]
        self.windowCenter = [x/len(self.window), y/len(self.window), z/len(self.window)]
        self.renderObjetcs()
        self.log.insert(0, "Window movida na direção "+direction)

    def rotateWindow(self, direction, axis):
        # 20 graus:
        angle = pi / 9
        if axis == 'x':
            self.windowRotate = self.windowRotate.dot(np.array([[1,0,0,0],[0,cos(angle),-sin(angle),0],[0,sin(angle),cos(angle),0],[0,0,0,1]]))
        elif axis == 'y':
            self.windowRotate = self.windowRotate.dot(np.array([[cos(angle),0,-sin(angle),0],[0,1,0,0],[sin(angle),0,cos(angle),0],[0,0,0,1]]))
        elif axis == 'z':
            self.windowRotate = self.windowRotate.dot(np.array([[cos(angle),-sin(angle),0,0],[sin(angle),cos(angle),0,0],[0,0,1,0],[0,0,0,1]]))

    def moveObject(self, direction):
        valorDeTranslacao = 0.1
        windowHeight = sqrt((self.window[3][0]-self.window[0][0])**2 + (self.window[3][1]-self.window[0][1])**2)/2
        valor = windowHeight * valorDeTranslacao
        try:
            obj = self.displayFile[self.listObjects.curselection()[0]]
            if direction == "↑":
                (Cx,Cy) = (0,valor)
            elif direction == "←":
                (Cx,Cy) = (-valor,0)
            elif direction == "↓":
                (Cx,Cy) = (0,-valor)
            elif direction == "→":
                (Cx,Cy) = (valor,0)
            aux = []
            for coordenada in obj.coordenadas:
                aux1 = np.array([[coordenada.x,coordenada.y,coordenada.z,1]])
                aux2 = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[Cx,Cy,0,1]])
                final = aux1.dot(aux2).tolist()
                aux.append(Coordenada(final[0][0],final[0][1],final[0][2]))
            obj.coordenadas = aux
            self.renderObjetcs()
            self.log.insert(0, obj.nome+" movido na direcao "+direction)
        except:
            self.log.insert(0, "Selecione um objeto primeiro.")

    def rotateObject(self, direction):
        try:
            obj = self.displayFile[self.listObjects.curselection()[0]]
            if self.opcaoCentroDeRotacao.get() == "Mundo":
                centro = np.array([0, 0])
            elif self.opcaoCentroDeRotacao.get() == "Objeto":
                centro = Operations.objectCenter(obj.worldCoordinates)
            else:
                centro = np.array([self.centroDeRotacaoX, self.centroDeRotacaoY])
            angle = pi / 9 if direction == "l" else -pi / 9
            obj.worldCoordinates = obj.worldCoordinates.dot(Operations.rotateMatrix(angle, centro))
            self.renderObjetcs()
            self.log.insert(0, obj.name+" rotacionado em "+str(ceil(angle*(180/pi)))+" graus na direção "+("↺" if direction == "l" else "↻")+" no "+str(self.opcaoCentroDeRotacao.get()))
        except:
            self.log.insert(0, "Selecione um objeto primeiro.")

    def scaleObject(self, tipo):
        obj = self.displayFile[self.listObjects.curselection()[0]]
        centro = Operations.objectCenter(obj.coordinates)
        z = 1.5 if tipo == "+" else 0.5
        obj.worldCoordinates = obj.worldCoordinates.dot(Operations.scaleMatrix([z, z], centro))
        self.renderObjetcs()
        self.log.insert(0, obj.name+(" ampliado" if tipo == "+" else " reduzido"))
    
    def removeObject(self):
        try:
            selectedObjectIndex = self.listObjects.curselection()[0]
            nome = self.displayFile[selectedObjectIndex].nome
            self.displayFile.pop(selectedObjectIndex)
            self.listObjects.delete(self.listObjects.curselection()[0])
            self.log.insert(0, "Objeto "+ nome + " removido")
            self.renderObjetcs()
        except:
            self.log.insert(0, "Selecione um objeto para Deletar.")
    
    def addObject(self):
        self.objectCoordinates = []
        self.newWindow = Toplevel(self.root)
        self.newWindow.title("Incluir Objeto")
        self.newWindow.geometry("500x300")
        self.newWindow.minsize(500, 300)
        # frame do nome:
        frameName = Frame(self.newWindow)
        frameName.pack(pady=(10, 0), fill=X)
        self.objectName = StringVar()
        Label(frameName, text="Nome ").pack(side=LEFT, pady=(0, 10), padx=(5, 0))
        Entry(frameName, textvariable=self.objectName, width=250).pack(side=LEFT, fill=X, pady=(0, 10), padx=(0, 10))
        
        self.tabControl = ttk.Notebook(self.newWindow)
        
        tabPonto = Frame(self.tabControl)
        tabPonto.pack(fill=Y, expand=1)
        tabReta = Frame(self.tabControl)
        self.tabWireframe = Frame(self.tabControl)
        self.tabControl.add(tabPonto, text='Ponto')
        self.tabControl.add(tabReta, text='Reta')
        self.tabControl.add(self.tabWireframe, text="Wireframe")

        # Ponto:
        framePonto = Frame(tabPonto)
        framePonto.pack(fill=BOTH)
        self.x1 = DoubleVar()
        self.y1 = DoubleVar()
        self.z1 = DoubleVar(value=0)
        Label(framePonto, text='X = ').grid(row=0, column=0)
        Entry(framePonto, textvariable=self.x1, width=13).grid(row=0, column=1)
        Label(framePonto, text='Y = ').grid(row=0, column=2)
        Entry(framePonto, textvariable=self.y1, width=13).grid(row=0, column=3)
        Label(framePonto, text='Z = ').grid(row=0, column=4)
        Entry(framePonto, textvariable=self.z1, width=13).grid(row=0, column=5)
        Button(framePonto, text="Incluir Ponto", bg="lightgreen", command=lambda: self.addCoordinates("Ponto")).grid(row=1, column=0, columnspan=10, sticky=W+E+N+S)
        
        # Reta:
        frameReta = Frame(tabReta)
        frameReta.pack(fill=X)
        self.x2 = DoubleVar()
        self.y2 = DoubleVar()
        self.z2 = DoubleVar(value=0)
        Label(frameReta, text='X1 = ').grid(row=0, column=0)
        Entry(frameReta, textvariable=self.x1, width=13).grid(row=0, column=1)
        Label(frameReta, text='Y1 = ').grid(row=0, column=2)
        Entry(frameReta, textvariable=self.y1, width=13).grid(row=0, column=3)
        Label(frameReta, text='Z1 = ').grid(row=0, column=4)
        Entry(frameReta, textvariable=self.z1, width=13).grid(row=0, column=5)
        Label(frameReta, text='X2 = ').grid(row=1, column=0)
        Entry(frameReta, textvariable=self.x2, width=13).grid(row=1, column=1)
        Label(frameReta, text='Y2 = ').grid(row=1, column=2)
        Entry(frameReta, textvariable=self.y2, width=13).grid(row=1, column=3)
        Label(frameReta, text='Z2 = ').grid(row=1, column=4)
        Entry(frameReta, textvariable=self.z2, width=13).grid(row=1, column=5)

        Button(frameReta, text="Incluir Reta", bg="lightgreen", command=lambda: self.addCoordinates("Reta")).grid(row=2, column=0, columnspan=10, sticky=W+E+N+S)
        
        # Wireframe:
        # Gambiarra PESADA feita aqui xD
        self.mudancas = 0
        self.frameWire = Frame(self.tabWireframe)
        self.frameWire.pack(fill=X)
        self.vertices = IntVar()
        self.vertices.trace("w", lambda x, y, z: [self.updateWireframeAdd(), self.updateMudancas()])
        Label(self.frameWire, text="Quantidade de Vértices do Wireframe: ").grid(row=0, column=0)
        Entry(self.frameWire, textvariable=self.vertices).grid(row=0, column=1)
        self.frameCoords = Frame(self.frameWire)
        self.frameCoords.grid(row=1, column=0, columnspan=2)

        # pack do tabControl (tem q ser depois de toda a config dos tabs)
        self.tabControl.pack(fill=BOTH)

    def updateMudancas(self):
        print('mudanca')
        self.mudancas += 1
        print('valor mudanca: '+str(self.mudancas))

    def updateWireframeAdd(self):
        # ele entra na função 2x devido ao trace (na hora que apaga e escreve valor)
        # na 1a entrada ele da um exception de tipo esperado int e encontra "". Não quebra nada
        # mas coloquei esse try/except só pra não encher o terminal de exceptions xD
        try:
            if self.mudancas > 2:
                self.frameCoords.grid_forget()
                self.frameCoords.destroy()
                self.frameCoords = Frame(self.frameWire)
                self.frameCoords.grid(row=1, column=0)
            self.wireFrameX = []
            self.wireFrameY = []
            self.wireFrameZ = []
            for i in range(self.vertices.get()):
                self.wireFrameX.append(DoubleVar())
                self.wireFrameY.append(DoubleVar())
                self.wireFrameZ.append(DoubleVar(value=0))
                Label(self.frameCoords, text="X"+str(i+1)+" = ").grid(row=i, column=0)
                Entry(self.frameCoords, textvariable=self.wireFrameX[i], width=10).grid(row=i, column=1)
                Label(self.frameCoords, text="Y"+str(i+1)+" = ").grid(row=i, column=2)
                Entry(self.frameCoords, textvariable=self.wireFrameY[i], width=10).grid(row=i, column=3)
                Label(self.frameCoords, text="Z"+str(i+1)+" = ").grid(row=i, column=4)
                Entry(self.frameCoords, textvariable=self.wireFrameZ[i], width=10).grid(row=i, column=5)
            Button(self.frameCoords, text="Incluir Wireframe", bg="lightgreen", command=lambda: self.addCoordinates("Wireframe")).grid(row=(self.vertices.get()), column=0)
        except:
            print("exception do updateWireframeAdd trollzinho")

    def addCoordinates(self, tipo):
        coordenadas = []
        self.root.update_idletasks()
        name = self.objectName.get()
        if (tipo == "Ponto"):
            self.log.insert(0, "Ponto")
            x = self.x1.get()
            y = self.y1.get()
            z = self.z1.get()
            coordenadas.append(Coordenada(x,y,z))
            self.displayFile.append(Ponto(name, coordenadas))
        elif (tipo == "Reta"):
            self.log.insert(0, "Reta")
            x1 = self.x1.get()
            y1 = self.y1.get()
            z1 = self.z1.get()
            x2 = self.x2.get()
            y2 = self.y2.get()
            z2 = self.z2.get()
            coordenadas.append(Coordenada(x1,y1,z1))
            coordenadas.append(Coordenada(x2,y2,z2))
            self.displayFile.append(Reta(name, coordenadas))
        elif (tipo == "Wireframe"):
            self.log.insert(0, "Wireframe")
            for i in range(self.vertices.get()):
                coordenadas.append(Coordenada(self.wireFrameX[i].get(), self.wireFrameY[i].get(), self.wireFrameZ[i].get()))
            self.displayFile.append(Wireframe(name, coordenadas))

        indiceItensRegistrados = len(self.displayFile)
        self.listObjects.insert(END, str(indiceItensRegistrados)+") " + name + "("+tipo+")")
        self.log.insert(0, "Objeto " + name + " incluido")
        
        self.renderObjetcs()
        self.newWindow.destroy()
