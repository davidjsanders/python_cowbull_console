import sys
if sys.version_info[0] < 3:
    import Tkinter as Tkinter
    from Tkinter import *
else:
    import tkinter as Tkinter
    from tkinter import *


class TkViewMenu(Tkinter.Menu):
    def __init__(self, parent, callback):
        Tkinter.Menu.__init__(self, parent)

        if not callback:
            print("Callback is {}".format(callback))
            raise TypeError("Callback class must be provided to file menu!")

        fileMenu = Tkinter.Menu(self)
        self.add_cascade(label="File", underline=0, menu=fileMenu)
        fileMenu.add_command(label="New Game", command=callback.instructions)
        fileMenu.add_command(label="Test", command=callback.instructions)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=callback.quit)

        helpmenu = Tkinter.Menu(self)
        self.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="Instructions", command=callback.instructions)

#        self.menu = TkViewMenu(self)
#        self = TkViewMenu(menu)
#        menu.add_cascade(label="File", menu=self)
#        self.add_command(label="New Game", command=callback.instructions)
#        self.add_separator()
#        self.add_command(label="Exit", command=callback.quit)

