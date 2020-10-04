# coding: utf-8
from tkinter import *
from tkinter import ttk
from sympy import Matrix
from math import sin, cos, pi, ceil

from Objects import Coordinates, Objeto
import Objects as Opr
from LiangBarsky import *


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
        self.window = Matrix.zeros(4, 3)
        self.window[0, 0:3] = Matrix([[self.canvas.winfo_width(), self.canvas.winfo_height(), 1]])
        self.window[1, 0:3] = Matrix([[self.canvas.winfo_width(), 0, 1]])
        self.window[2, 0:3] = Matrix([[0, 0, 1]])
        self.window[3, 0:3] = Matrix([[0, self.canvas.winfo_height(), 1]])
        self.windowTransform = Matrix.eye(3)
        self.windowRotation = 0
        self.vUpVector = Opr.viewUpVector(self.windowRotation)
        self.vRightVector = Opr.viewRightVector(self.windowRotation)

        # Lista de objetos:
        self.displayFile = []

        # Inicializa:
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
        Button(frameDirecoes, text="↑", command=lambda: self.moveWindow("n")).grid(row=0, column=1)
        Button(frameDirecoes, text="←", command=lambda: self.moveWindow("w")).grid(row=1, column=0)
        Button(frameDirecoes, text="↓", command=lambda: self.moveWindow("s")).grid(row=1, column=1)
        Button(frameDirecoes, text="→", command=lambda: self.moveWindow("e")).grid(row=1, column=2)
        Button(frameZoom, text="+", command=lambda: self.zoomWindow("+")).grid(row=0, column=0)
        Button(frameZoom, text="-", command=lambda: self.zoomWindow("-")).grid(row=1, column=0)
        Button(frameDirecoes, text="↺", command=lambda: self.rotateWindow("l")).grid(row=2, column=0)
        Button(frameDirecoes, text="↻", command=lambda: self.rotateWindow("r")).grid(row=2, column=2)

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
        Button(frameTranslacao, text="↑", command=lambda: self.moveObject("n")).grid(row=0, column=1)
        Button(frameTranslacao, text="←", command=lambda: self.moveObject("w")).grid(row=1, column=0)
        Button(frameTranslacao, text="↓", command=lambda: self.moveObject("s")).grid(row=1, column=1)
        Button(frameTranslacao, text="→", command=lambda: self.moveObject("e")).grid(row=1, column=2)
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

        # move o mundo de acordo com o ponto de vista da window e clippa os objetos
        self.window *= self.windowTransform
        normalize = Opr.objectNormalizationMatrix(self.window, self.windowRotation)
        normalizedWindow = self.window * normalize
        clpWndw = Matrix([0.875 * normalizedWindow[2, 0:2], 0.875 * normalizedWindow[0, 0:2]])

        for o in self.displayFile:
            o.windowCoordinates = o.worldCoordinates * normalize
            renderingCoordinates = []
            line = []
            pointsNum = len(o.windowCoordinates[:, 0])
            for i in range(pointsNum):
                point = o.windowCoordinates.row(i)
                line.append(point)
                if len(line) == 2:
                    cleanLine = Matrix(line)[0:2, 0:2]
                    clipped = clipLine(clpWndw, cleanLine)
                    print("Clipped: " + str(clipped))
                    if clipped is not None:
                        renderingCoordinates.append(clipped)
                    line.pop(0)
            lastLine = Matrix([o.windowCoordinates[pointsNum - 1, 0:2], o.windowCoordinates[0, 0:2]])
            lastLineClipped = cleanLine(clpWndw, lastLine)
            if lastLineClipped is not None:
                renderingCoordinates.append(lastLineClipped)
            print("Rendering coordinates: " + str(renderingCoordinates))
            o.windowCoordinates = Matrix(renderingCoordinates)
            print(" * in Matrix form: " + str(o.windowCoordinates))

        # inicio transformada de ViewPort:
        self.objetosTransformados = []
        # limites ViewPort:
        Xvpmin = 0
        Yvpmin = 0
        Xvpmax = self.canvas.winfo_width()
        Yvpmax = self.canvas.winfo_height()
        # Limites da Window:
        Xwmin = -1
        Ywmin = -1
        Xwmax = 1
        Ywmax = 1

        tvpx = lambda x: Opr.transformViewPortX(x, Xwmin, Xwmax, Xvpmax, Xvpmin)
        tvpy = lambda y: Opr.transformViewPortY(y, Ywmin, Ywmax, Yvpmax, Yvpmin)
        for o in self.displayFile:
            for i in range(len(o.windowCoordinates[:, 0])):
                o.windowCoordinates[i, 0] = tvpx(o.windowCoordinates[i, 0])
                o.windowCoordinates[i, 1] = tvpy(o.windowCoordinates[i, 1])
            print(o.windowCoordinates)
        # fim transformada de ViewPort
        # inicio desenho no canvas:
        for o in self.displayFile:
            if o.tipo == 'Reta' or o.tipo == 'Wireframe':
                coords = []
                for i in range(len(o.windowCoordinates[:,0])):
                    row = o.windowCoordinates[i]
                    coords += [row[0], row[1]]
                # precisa incluir a primeira coordenada de novo pra que seja feita a linha tbm da ultima coordenada com a primeira:
                coords += [o.windowCoordinates[0, 0], o.windowCoordinates[0, 1]]
                self.canvas.create_line(coords)
            else:
                x = o.windowCoordinates[0, 0]
                y = o.windowCoordinates[0, 1]
                self.canvas.create_oval(x - 0.5, y - 0.5, x + 0.5, y + 0.5)
        # fim desenho no canvas

    def zoomWindow(self, tipo):
        operador = 1.25 if tipo == "+" else 1 / 1.25
        self.windowTransform *= Opr.scaleMatrix(operador, Opr.objectCenter(self.window))
        self.log.insert(0, "zoom "+tipo+" na Window")
        self.renderObjetcs()

    def moveWindow(self, direction):
        tValue = 20
        if direction == "n":
            self.windowTransform *= Opr.translateMatrix(tValue * self.vUpVector)
        elif direction == "w":
            self.windowTransform *= Opr.translateMatrix(-tValue * self.vRightVector)
        elif direction == "s":
            self.windowTransform *= Opr.translateMatrix(-tValue * self.vUpVector)
        elif direction == "e":
            self.windowTransform *= Opr.translateMatrix(* tValue * self.vRightVector)
        self.renderObjetcs()
        self.log.insert(0, "Window movida na direção "+direction)

    def rotateWindow(self, direction):
        angle = pi / 9 if direction == "l" else -pi / 9
        self.windowTransform *= Opr.rotateMatrix(angle, Opr.objectCenter(self.window))
        self.windowRotation += angle
        self.vUpVector = Opr.viewUpVector(self.windowRotation)
        self.vRightVector = Opr.viewRightVector(self.windowRotation)

    def moveObject(self, direction):
        valorDeTranslacao = 10
        try:
            obj = self.displayFile[self.listObjects.curselection()[0]]
            # cria matriz identidade 3x3:
            tMatrix = Matrix.eye(3)
            if direction == "n":
                tMatrix[2, 1] = valorDeTranslacao
            elif direction == "w":
                tMatrix[2, 0] = -valorDeTranslacao
            elif direction == "s":
                tMatrix[2, 1] = -valorDeTranslacao
            elif direction == "e":
                tMatrix[2, 0] = valorDeTranslacao
            nobj = Opr.genericTransformation(obj, tMatrix)
            self.displayFile[self.listObjects.curselection()[0]] = nobj
            self.renderObjetcs()
            self.log.insert(0, obj.name+" movido na direcao "+direction)
        except:
            self.log.insert(0, "Selecione um objeto primeiro.")

    def rotateObject(self, direction):
        valorDeRotacao = pi/3
        try:
            obj = self.displayFile[self.listObjects.curselection()[0]]
            if self.opcaoCentroDeRotacao.get() == "Mundo":
                centro = Coordinates(0, 0)
            elif self.opcaoCentroDeRotacao.get() == "Objeto":
                centro = Opr.polygonCenter(obj.coordinates)
            else:
                centro = Coordinates(float(self.centroDeRotacaoX.get()), float(self.centroDeRotacaoY.get()))
            mMatrix = Matrix.eye(3)
            mMatrix[2, 0] = -centro.x
            mMatrix[2, 1] = -centro.y
            rotacao = 1 if direction == "r" else -1
            rMatrix = Matrix.eye(3)
            c = cos(rotacao * valorDeRotacao)
            s = sin(rotacao * valorDeRotacao)
            rMatrix[0, 0] = c
            rMatrix[0, 1] = -s
            rMatrix[1, 1] = c
            rMatrix[1, 0] = s
            bMatrix = Matrix.eye(3)
            bMatrix[2, 0] = centro.x
            bMatrix[2, 1] = centro.y
            tMatrix = mMatrix * rMatrix * bMatrix
            nobj = Opr.genericTransformation(obj, tMatrix)
            self.displayFile[self.listObjects.curselection()[0]] = nobj
            self.renderObjetcs()
            self.log.insert(0, obj.name+" rotacionado em "+str(ceil(valorDeRotacao*(180/pi)))+" graus na direção "+("↺" if direction == "l" else "↻")+" no "+str(self.opcaoCentroDeRotacao.get()))
        except:
            self.log.insert(0, "Selecione um objeto primeiro.")

    def scaleObject(self, tipo):
        obj = self.displayFile[self.listObjects.curselection()[0]]
        centro = Opr.polygonCenter(obj.coordinates)
        mMatrix = Matrix.eye(3)
        mMatrix[2, 0] = -centro.x
        mMatrix[2, 1] = -centro.y
        z = 1.5 if tipo == "+" else 0.5
        sMatrix = Matrix.eye(3)
        sMatrix[0, 0] = z
        sMatrix[1, 1] = z
        bMatrix = Matrix.eye(3)
        bMatrix[2, 0] = centro.x
        bMatrix[2, 1] = centro.y
        tMatrix = mMatrix * sMatrix * bMatrix
        nobj = Opr.genericTransformation(obj, tMatrix)
        self.displayFile[self.listObjects.curselection()[0]] = nobj
        self.renderObjetcs()
        self.log.insert(0, obj.name+(" ampliado" if tipo == "+" else " reduzido"))
    
    def removeObject(self):
        self.log.insert(0, "Objeto "+self.displayFile[(self.listObjects.curselection()[0])].name + " removido")
        self.displayFile.pop(self.listObjects.curselection()[0])
        self.listObjects.delete(self.listObjects.curselection()[0])
        self.renderObjetcs()
    
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
        Label(framePonto, text='X = ').grid(row=0, column=0)
        Entry(framePonto, textvariable=self.x1, width=13).grid(row=0, column=1)
        Label(framePonto, text='Y = ').grid(row=0, column=2)
        Entry(framePonto, textvariable=self.y1, width=13).grid(row=0, column=3)
        Button(framePonto, text="Incluir Ponto", bg="lightgreen", command=lambda: self.addCoordinates("Ponto")).grid(row=1, column=0, columnspan=10, sticky=W+E+N+S)
        
        # Reta:
        frameReta = Frame(tabReta)
        frameReta.pack(fill=X)
        self.x2 = DoubleVar()
        self.y2 = DoubleVar()
        Label(frameReta, text='X1 = ').grid(row=0, column=0)
        Entry(frameReta, textvariable=self.x1, width=13).grid(row=0, column=1)
        Label(frameReta, text='Y1 = ').grid(row=0, column=2)
        Entry(frameReta, textvariable=self.y1, width=13).grid(row=0, column=3)
        Label(frameReta, text='X2 = ').grid(row=1, column=0)
        Entry(frameReta, textvariable=self.x2, width=13).grid(row=1, column=1)
        Label(frameReta, text='Y2 = ').grid(row=1, column=2)
        Entry(frameReta, textvariable=self.y2, width=13).grid(row=1, column=3)
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
            for i in range(self.vertices.get()):
                self.wireFrameX.append(DoubleVar())
                self.wireFrameY.append(DoubleVar())
                Label(self.frameCoords, text="X"+str(i+1)+" = ").grid(row=i, column=0)
                Entry(self.frameCoords, textvariable=self.wireFrameX[i], width=10).grid(row=i, column=1)
                Label(self.frameCoords, text="Y"+str(i+1)+" = ").grid(row=i, column=2)
                Entry(self.frameCoords, textvariable=self.wireFrameY[i], width=10).grid(row=i, column=3)
            Button(self.frameCoords, text="Incluir Wireframe", bg="lightgreen", command=lambda: self.addCoordinates("Wireframe")).grid(row=(self.vertices.get()), column=0)
        except:
            print("exception do updateWireframeAdd trollzinho")

    def addCoordinates(self, tipo):
        #  TODO: refatorar que depois q fiz o wireframe da pra deixar bem melhor
        name = self.objectName.get()
        if (tipo == "Ponto"):
            self.log.insert(0, "Ponto")
            x = self.x1.get()
            y = self.y1.get()
            self.objectCoordinates.append([x, y, 1])
            quantidade = 1
        elif (tipo == "Reta"):
            self.log.insert(0, "Reta")
            x1 = self.x1.get()
            y1 = self.y1.get()
            x2 = self.x2.get()
            y2 = self.y2.get()
            self.objectCoordinates.append([x1, y1, 1])
            self.objectCoordinates.append([x2, y2, 1])
            quantidade = 2
        elif (tipo == "Wireframe"):
            self.log.insert(0, "Wireframe")
            quantidade = self.vertices.get()
            for i in range(quantidade):
                self.objectCoordinates.append([self.wireFrameX[i].get(), self.wireFrameY[i].get(), 1])
        
        objeto = Objeto(name, Matrix(self.objectCoordinates), tipo, quantidade)
        indiceItensRegistrados = len(self.displayFile)
        self.listObjects.insert(END, str(indiceItensRegistrados)+") " + objeto.name + "("+objeto.tipo+")")
        self.log.insert(0, "Objeto " + objeto.name + " incluido")
        self.displayFile.append(objeto)
        
        self.renderObjetcs()
        self.newWindow.destroy()
