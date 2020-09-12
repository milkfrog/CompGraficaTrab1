from tkinter import *
from tkinter import ttk
from math import *
from Objects import Coordenates, Objeto


class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("Trabalho 1 de Computação Gráfica INE5420")
        self.root.geometry("1200x700")
        self.root.minsize(1200, 700)

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
        Button(frameDirecoes, text="↑").grid(row=0, column=1)
        Button(frameDirecoes, text="←").grid(row=1, column=0)
        Button(frameDirecoes, text="↓").grid(row=1, column=1)
        Button(frameDirecoes, text="→").grid(row=1, column=2)
        Button(frameZoom, text="+").grid(row=0, column=0)
        Button(frameZoom, text="-").grid(row=1, column=0)

        # frame da ViewPort:
        frameViewPort = LabelFrame(self.root, text="ViewPort")
        frameViewPort.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(frameViewPort, bg="#fff")
        self.canvas.pack(fill=BOTH, expand=1)

        # frame de Log:
        frameLog = LabelFrame(frameViewPort, text="Log")
        frameLog.pack(fill=X, side=BOTTOM)
        self.log = Listbox(frameLog, height=5)
        self.log.pack(fill=X)

    def renderObjetcs(self):
        for i in self.displayFile:
            if (i.tipo == 'Reta'):
                coordenadas = []
                for coord in i.coordenates:
                    coordenadas += [coord.x, coord.y]
                coords += [i.coordenates[0].x, i.coordenates[0].y]
                self.canvas.create_line(coords, tags=i.name)
            else:
                self.canvas.create_oval(i.coordenates[0].x - 1, i.coordenates[0].y - 1, i.coordenates[0].x + 1, i.coordenates[0].y + 1)

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
        
        tabControl = ttk.Notebook(self.newWindow)
        
        tabPonto = Frame(tabControl)
        tabPonto.pack(fill=Y, expand=1)
        tabReta = Frame(tabControl)
        tabWireframe = Frame(tabControl)
        tabControl.add(tabPonto, text='Ponto')
        tabControl.add(tabReta, text='Reta')
        tabControl.add(tabWireframe, text="Wireframe")

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
        frameWire = Frame(tabWireframe)
        frameWire.pack(fill=X)
        Button(frameWire, text="Incluir Wireframe", bg="lightgreen", command=lambda: self.addCoordenates("Wireframe")).pack(side=BOTTOM)

        
        # pack do tabControl (tem q ser depois de toda a config dos tabs)
        tabControl.pack(fill=BOTH)
        
        # frame de incluir objeto:
        # frameIncludeObject = Frame(self.newWindow)
        # frameIncludeObject.pack(side=BOTTOM)
        # Button(frameIncludeObject, text="Incluir Objeto", bg="lightgreen", command=self.addCoordenates).pack()


    def addCoordenates(self, tipo):
        name = self.objectName.get()
        if (tipo == "Ponto"):
            self.log.insert(0, "Ponto")
            x = self.x1.get()
            y = self.y1.get()
            self.objectCoordenates.append(Coordenates(x, y))
            ponto = Objeto(name, self.objectCoordenates ,tipo)
            # refatorar pra mostrar mais bonitinho na lista:
            self.listObjects.insert(END, ponto.name)
            self.log.insert(0, "Objeto "+ ponto.name + " incluido")
            self.displayFile.append(ponto)
            self.renderObjetcs()
            self.newWindow.destroy()
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
        
        self.log.insert(0, "coords: " + str(self.objectCoordenates[len(self.objectCoordenates)-1]))
        