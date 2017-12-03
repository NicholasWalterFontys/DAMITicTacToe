import tkinter

instance = None


def get_instance():
    global instance
    if instance is None:
        instance = Visualizer()
    return instance


class Visualizer:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title = "Tic Tac Toe AI Visualizer"
        background = tkinter.Frame(master=self.root, width=620, heigh=620)

        self.strings = [None] * 9

        for i in range(3):
            for j in range(3):
                index = i + j * 3
                stringvar = tkinter.StringVar()
                stringvar.set("")
                b = tkinter.Button(master=background, textvariable=stringvar,
                                   #height=200, width=200,
                                   command=lambda index=index: self.button_callback(index))
                x = i * 210
                y = j * 210
                b.place(x=x, y=y)
                self.strings[index] = stringvar

        background.pack()
        self.root.mainloop()

    def button_callback(self, index):
        print("button callback index: " + str(index))
        self.strings[index].set("clicked")

if __name__ == "__main__":
    a = get_instance()
