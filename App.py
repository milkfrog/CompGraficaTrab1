from tkinter import *

class App:
  def __init__(self):
    self.root = Tk()
    self.root.title("teewexxxxte")

    lastx, lasty = 0, 0

    def xy(event):
      global lastx, lasty
      lastx, lasty = event.x, event.y

    def addLine(event):
      global lastx, lasty
      canvas.create_line((lastx, lasty, event.x, event.y))
      lastx, lasty = event.x, event.y

    self.root.columnconfigure(0, weight=1)
    self.root.rowconfigure(0, weight=1)

    canvas = Canvas(self.root)
    canvas.grid(column=0, row=0, sticky=(N, W, E, S))
    canvas.bind("<Button-1>", xy)
    # canvas.bind("<B1-Motion>", addLine)

    self.root.mainloop()