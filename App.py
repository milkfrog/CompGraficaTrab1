from tkinter import *


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
        log = Listbox(frameLog, height=5)
        log.pack(fill=X)

    def renderObjetc(self):
        pass

    def addObject(self):
        coordenadasObjeto = []
        newWindow = Toplevel(self.root)
        newWindow.title("Incluir Objeto")
        newWindow.geometry("300x300")
        newWindow.minsize(300, 300)

        