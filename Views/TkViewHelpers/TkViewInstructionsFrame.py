import sys
if sys.version_info[0] < 3:
    import Tkinter as Tkinter
    from Tkinter import *
else:
    import tkinter as Tkinter
    from tkinter import *


class TkViewInstructionsFrame(Tkinter.LabelFrame):
    def __init__(self, parent, welcome_message=None, *args, **kwargs):
        Tkinter.LabelFrame.__init__(self, parent, text="Instructions", *args, **kwargs)

        self.text = "Instructions"

        self.instruction_text = Text(self)
        self.instruction_text.tag_config("textformat", borderwidth=3, wrap=WORD)
        self.instruction_text.insert(INSERT, welcome_message, ("textformat"))
        self.instruction_text.config(
            state=DISABLED,
            height=1,
            font=("Helvetica", 16),
            borderwidth=7
        )
        self.instruction_text.grid(row=0, column=0, ipadx=10, ipady=5, sticky=N + S + E + W)

        self.grid()
        Grid.rowconfigure(self, 0, weight=0, minsize=100)
        Grid.columnconfigure(self, 0, weight=1)
