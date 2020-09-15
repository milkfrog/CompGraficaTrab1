# coding: utf-8
from tkinter import *
from tkinter import ttk
from sympy import Matrix
from math import sin, cos, pi

from Objects import Coordenates, Objeto, Operations


class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("Trabalho 1 de Computação Gráfica INE5420")
        # limitando o tamanho do App em 1200x800
        self.root.minsize(1200, 800)
        self.root.maxsize(1200, 800)

        # Configs iniciais:
        self.windowZoomX = 0
        self.windowZoomY = 0
        self.windowTransferX = 0
        self.windowTransferY = 0

        # render frame do Widget:
        self.renderWidget()

        # Variáveis globais:
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
        frameRemoveAdd.pack(pady=(10,0))
        Button(frameRemoveAdd, text="Incluir Objeto", bg="lightgreen", command=self.addObject).pack(side=LEFT, padx=(5,15))
        Button(frameRemoveAdd, text="Remover Objeto", bg="#ffcccb").pack(side=RIGHT, padx=(0,5))
        
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

        # frame de Transformacao de Objetos
        self.opcaoCentroDeRotacao = StringVar()
        opcoesCentroDeRotacao = {'Mundo', 'Objeto', 'Ponto Qualquer'}
        self.opcaoCentroDeRotacao.set('Objeto')
        self.centroDeRotacaoX = DoubleVar()
        self.centroDeRotacaoY = DoubleVar()
        labelTransformacoes = LabelFrame(menuDeFuncoes, text="Trasformacao de Objetos", width=100)
        labelTransformacoes.pack(side=TOP, fill=X, pady=(10,0))
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

    def renderObjetcs(self):
        # deletando o que tiver desenhado no canvas:
        self.canvas.delete("all")
        # calculando as variaveis da transformada de ViewPort:
        self.objetosTransformados = []
        # limites ViewPort:
        Xvpmin = 0 - self.windowZoomX
        Yvpmin = 0 - self.windowZoomY
        Xvpmax = self.canvas.winfo_width() + self.windowZoomX
        Yvpmax = self.canvas.winfo_height() + self.windowZoomY
        # Limites da Window:
        Xwmin = 0 + self.windowTransferX
        Ywmin = 0 + self.windowTransferY
        Xwmax = self.canvas.winfo_width() + self.windowTransferX
        Ywmax = self.canvas.winfo_height() + self.windowTransferY
        for i in self.displayFile:
            listCoordenatesTransformed = []
            for coords in i.coordenates:
                Xvp = Operations.transformViewPortX(self, coords.x, Xwmin, Xwmax, Xvpmax, Xvpmin)
                Yvp = Operations.transformViewPortY(self, coords.y, Ywmin, Ywmax, Yvpmax, Yvpmin)
                listCoordenatesTransformed.append(Coordenates(Xvp, Yvp))
            objectTransformed = Objeto(i.name, listCoordenatesTransformed ,i.tipo)
            self.objetosTransformados.append(objectTransformed)
        for i in self.objetosTransformados:
            if (i.tipo == 'Reta' or i.tipo == 'Wireframe'):
                coords = []
                for coordXY in i.coordenates:
                    coords += [coordXY.x, coordXY.y] 
                # precisa incluir a primeira coordenada de novo pra que seja feita a linha tbm da ultima coordenada com a primeira:
                coords += [i.coordenates[0].x, i.coordenates[0].y]
                self.canvas.create_line(coords)
            else:
                self.canvas.create_oval(i.coordenates[0].x - 0.5, i.coordenates[0].y - 0.5, i.coordenates[0].x + 0.5, i.coordenates[0].y + 0.5)

    def zoomWindow(self, tipo):
        operador = +1 if tipo == "+" else -1
        self.windowZoomX += operador * self.canvas.winfo_width() * 0.05
        self.windowZoomY += operador * self.canvas.winfo_height() * 0.05
        self.log.insert(0, "zoom "+tipo+" na Window")
        self.renderObjetcs()

    def moveWindow(self, direction):
        if (direction == "n"):
            self.windowTransferY += 10
        elif (direction == "w"):
            self.windowTransferX -= 10
        elif (direction == "s"):
            self.windowTransferY -= 10
        elif (direction == "e"):
            self.windowTransferX += 10
        self.renderObjetcs()
        self.log.insert(0, "Window movida na direção "+direction)

    def moveObject(self, direction):
        obj = self.displayFile[self.listObjects.curselection()[0]]
        tMatrix = Matrix.eye(3)
        if (direction == "n"):
            tMatrix[2,1] = 10
        elif (direction == "w"):
            tMatrix[2,0] = -10
        elif (direction == "s"):
            tMatrix[2,1] = -10
        elif (direction == "e"):
            tMatrix[2,0] = 10
        nobj = Operations.genericTransformation(self, obj, tMatrix)
        self.displayFile[self.listObjects.curselection()[0]] = nobj
        self.renderObjetcs()
        self.log.insert(0, obj.name+" movido na direcao "+direction)


    def rotateObject(self, direction):
        obj = self.displayFile[self.listObjects.curselection()[0]]
        if (self.opcaoCentroDeRotacao.get() == "Mundo"):
            centro = Coordenates(0,0)
        elif (self.opcaoCentroDeRotacao.get() == "Objeto"):
            centro = Operations.polygonCenter(self, obj.coordenates)
        else:
            centro = Coordenates(float(self.centroDeRotacaoX.get()), float(self.centroDeRotacaoY.get()))
        mMatrix = Matrix.eye(3)
        mMatrix[2,0] = -centro.x
        mMatrix[2,1] = -centro.y
        dir = 1 if direction == "r" else -1
        rMatrix = Matrix.eye(3)
        c = cos(dir * pi/3)
        s = sin(dir * pi/3)
        rMatrix[0,0] = c
        rMatrix[0,1] = -s
        rMatrix[1,1] = c
        rMatrix[1,0] = s
        bMatrix = Matrix.eye(3)
        bMatrix[2,0] = centro.x
        bMatrix[2,1] = centro.y
        tMatrix = mMatrix * rMatrix * bMatrix
        nobj = Operations.genericTransformation(self, obj, tMatrix)
        self.displayFile[self.listObjects.curselection()[0]] = nobj
        self.renderObjetcs()
        self.log.insert(0, obj.name+" ampliado na direcao "+direction)

    def scaleObject(self, tipo):
        obj = self.displayFile[self.listObjects.curselection()[0]]
        centro = Operations.polygonCenter(self, obj.coordenates)
        mMatrix = Matrix.eye(3)
        mMatrix[2,0] = -centro.x
        mMatrix[2,1] = -centro.y
        z = 1.5 if tipo == "+" else 0.5
        sMatrix = Matrix.eye(3)
        sMatrix[0,0] = z
        sMatrix[1,1] = z
        bMatrix = Matrix.eye(3)
        bMatrix[2,0] = centro.x
        bMatrix[2,1] = centro.y
        tMatrix = mMatrix * sMatrix * bMatrix
        nobj = Operations.genericTransformation(self, obj, tMatrix)
        self.displayFile[self.listObjects.curselection()[0]] = nobj
        self.renderObjetcs()
        self.log.insert(0, obj.name+"  na direcao "+tipo)
    
    def addObject(self):
        self.objectCoordenates = []
        self.newWindow = Toplevel(self.root)
        self.newWindow.title("Incluir Objeto")
        self.newWindow.geometry("300x300")
        self.newWindow.minsize(300, 300)
        # frame do nome:
        frameName = Frame(self.newWindow)
        frameName.pack(pady=(10,0), fill=X)
        self.objectName = StringVar()
        Label(frameName, text="Nome ").pack(side=LEFT, pady=(0,10), padx=(5,0))
        Entry(frameName, textvariable=self.objectName, width=250).pack(side=LEFT, fill=X, pady=(0,10), padx=(0,10))
        
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
        Button(framePonto, text="Incluir Ponto", bg="lightgreen", command=lambda: self.addCoordenates("Ponto")).grid(row=1, column=0, columnspan=10, sticky=W+E+N+S)
        
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
        Button(frameReta, text="Incluir Reta", bg="lightgreen", command=lambda: self.addCoordenates("Reta")).grid(row=2, column=0, columnspan=10, sticky=W+E+N+S)
        
        # Wireframe:
        # Gambiarra PESADA feita aqui xD
        self.mudancas = 0
        self.frameWire = Frame(self.tabWireframe)
        self.frameWire.pack(fill=X)
        self.vertices = IntVar()
        self.vertices.trace("w", lambda x,y,z: [self.updateWireframeAdd(), self.updateMudancas()])
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
            if (self.mudancas > 2):
                self.frameCoords.grid_forget()
                self.frameCoords.destroy()
                self.frameCoords = Frame(self.frameWire)
                self.frameCoords.grid(row=1, column=0)
            print("número de vértices: "+str(self.vertices.get()))
            self.wireFrameX = []
            self.wireFrameY = []
            for i in range(self.vertices.get()):
                self.wireFrameX.append(DoubleVar())
                self.wireFrameY.append(DoubleVar())
                Label(self.frameCoords, text="X"+str(i+1)+" = ").grid(row=i, column=0)
                Entry(self.frameCoords, textvariable=self.wireFrameX[i], width=10).grid(row=i, column=1)
                Label(self.frameCoords, text="Y"+str(i+1)+" = ").grid(row=i, column=2)
                Entry(self.frameCoords, textvariable=self.wireFrameY[i], width=10).grid(row=i, column=3)
            Button(self.frameCoords, text="Incluir Wireframe", bg="lightgreen", command=lambda: self.addCoordenates("Wireframe")).grid(row=(self.vertices.get()), column=0)
        except:
            print("exception do updateWireframeAdd trollzinho")

    def addCoordenates(self, tipo):
        #  TODO: refatorar que depois q fiz o wireframe da pra deixar bem melhor
        name = self.objectName.get()
        if (tipo == "Ponto"):
            self.log.insert(0, "Ponto")
            x = self.x1.get()
            y = self.y1.get()
            self.objectCoordenates.append(Coordenates(x, y))
        elif (tipo == "Reta"):
            self.log.insert(0, "Reta")
            x1 = self.x1.get()
            y1 = self.y1.get()
            x2 = self.x2.get()
            y2 = self.y2.get()
            self.objectCoordenates.append(Coordenates(x1, y1))
            self.objectCoordenates.append(Coordenates(x2, y2))
        elif (tipo == "Wireframe"):
            self.log.insert(0, "Wireframe")
            for i in range(self.vertices.get()):
                self.objectCoordenates.append(Coordenates(self.wireFrameX[i].get(), self.wireFrameY[i].get()))
        
        objeto = Objeto(name, self.objectCoordenates ,tipo)
        indiceItensRegistrados = len(self.displayFile)
        self.listObjects.insert(END, str(indiceItensRegistrados)+") "+objeto.name+"("+objeto.tipo+")")
        self.log.insert(0, "Objeto "+ objeto.name + " incluido")
        self.displayFile.append(objeto)
        self.renderObjetcs()
        self.newWindow.destroy()    
        
        