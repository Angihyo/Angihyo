from tkinter import *

class counteer:
    def __init__(self):
        window = Tk()
        window.title("타이틀")
        fm = Frame(window)
        fm.pack()
        self.counter = 0
        self.result = StringVar()
        self.result.set(0)
        btup = Button(fm,text = "UP", width = 20, height = 5, command = self.add)
        btdown = Button(fm,text = "DOWN", width = 20, height = 5, command = self.sub)
        btreset = Button(fm, text = "RESET" ,  width = 20, height = 5, command = self.reset)
        lb = Label(window, textvariable = self.result, font = ("Times",24),)

        btup.pack(side = LEFT)
        btdown.pack(side = LEFT)
        btreset.pack(side = LEFT)
        lb.pack()

        window.mainloop()
    def add(self):
        if self.counter < 7:
            self.counter += 1
            self.result.set(self.counter)
    def sub(self):
        if self.counter > 0:
            self.counter -= 1
            self.result.set(self.counter)

    def reset(self):
        self.counter = 0
        self.result.set(0)

counteer()
#a = counteer.counter()

