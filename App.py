from tkinter import *


class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("Programinha Top")
        self.root.geometry("1000x500")

        teste = Frame(self.root, width=50)

        Label(teste, text="testeee", fg="black", bg="green")

        self.root.mainloop()

    def constructLayout():
        pass


