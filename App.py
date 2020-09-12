from tkinter import *


class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("Trabalho 1 de Computação Gráfica INE5420")
        self.root.geometry("1200x700")

        self.renderMenuDeFuncoes()

        self.root.mainloop()

    def renderMenuDeFuncoes(self):
        menuDeFuncoes = LabelFrame(self.root, text="Menu de Funções", width=100)
        labelObjetos = Label(menuDeFuncoes, text="Objetos")
        menuDeFuncoes.pack(side=LEFT, fill=Y)
        labelObjetos.pack(side=TOP)
        self.listObjects = Listbox(menuDeFuncoes, width=40, selectmode=SINGLE)
        self.listObjects.pack(side=TOP)
        