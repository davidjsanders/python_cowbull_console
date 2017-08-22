import sys
if sys.version_info[0] < 3:
    import Tkinter as Tkinter
    from Tkinter import *
else:
    import tkinter as Tkinter
    from tkinter import *


class TkViewButtons(object):
    @property
    def buttons(self):
        return self._buttons

    def __init__(self, parent, callback):
        if not parent:
            raise ValueError("Root frame must be passed for buttons!")

        if not callback:
            print("Callback is {}".format(callback))
            raise TypeError("Callback class must be provided to file menu!")

        self._buttons = dict(
            guess_btn=None,
            instructions_btn= None,
            quit_btn= None
        )

        self._buttons["guess_btn"] = Button(parent, text="Guess", command=callback.instructions)
#        self._buttons["guess_btn"].pack(side=LEFT)
        self._buttons["guess_btn"].grid(row=0, column=0, sticky=W)

        self._buttons["instructions_btn"] = Button(parent, text="Instructions", command=callback.instructions)
#        self._buttons["instructions_btn"].pack(side=LEFT)
        self._buttons["instructions_btn"].grid(row=0, column=1, sticky=W)

        self._buttons["quit_btn"] = Button(parent, text="QUIT", fg="red", command=callback.quit)
        self._buttons["quit_btn"].pack(side=LEFT)
        self._buttons["quit_btn"].grid(row=0, column=2, sticky=W)
