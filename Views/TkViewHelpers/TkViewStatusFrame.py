import sys
if sys.version_info[0] < 3:
    import Tkinter as Tkinter
    from Tkinter import *
else:
    import tkinter as Tkinter
    from tkinter import *


class TkViewStatusFrame(Tkinter.Frame):
    def __init__(self, parent, status=None, *args, **kwargs):
        Tkinter.Frame.__init__(self, parent, *args, **kwargs)

        self.text = Label(self)
        self.text.config(
            text=status,
            font=("Helvetica", 16),
            background="blue",
            foreground="white"
        )
        self.text.grid(row=0, column=0, ipadx=2, ipady=2, sticky=N+S+W)

        self.grid()
        Grid.rowconfigure(self, 0, weight=0, minsize=40)
        Grid.columnconfigure(self, 0, weight=1)

    def set_text(self, status=None):
        self.text.config(
            text=status,
            height=1,
            font=("Helvetica", 16),
            background="blue",
            foreground="white",
            justify=LEFT
        )
