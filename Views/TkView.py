import sys
from AbstractClasses.IO import IO

if sys.version_info[0] < 3:
    from Tkinter import *
else:
    from tkinter import *


class TkView(IO):
    def __init__(self):
        super(TkView, self).__init__()

    def say_hi(self):
        print("hi there, everyone!")

    def instructions(self, instruction_text=None, info_text=None, author=None):
        print(TkView.info_msg)

    def report_status(self, message=None):
        pass

    def want_to_play(self):
        pass

    def report_error(self, error_detail=None):
        pass

    def update_result(self, line_number=None, result=None, numbers_guessed=None):
        pass

    def finish(self, finish_message=None):
        pass

    def setup(self, game_tries=None):
        self.root = Tk()
        frame = Frame(self.root)
        frame.pack()

        menu = Menu(self.root)
        self.root.config(menu=menu)

        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New Game", command=self.say_hi)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=frame.quit)

        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="Instructions", command=self.instructions)

        self.guess_btn = Button(frame, text="Guess", command=self.instructions)
        self.guess_btn.pack(side=LEFT)

        self.instructions_btn = Button(frame, text="Instructions", command=self.instructions)
        self.instructions_btn.pack(side=LEFT)

        self.quit_btn = Button(
            frame, text="QUIT", fg="red", command=frame.quit
        )
        self.quit_btn.pack(side=LEFT)
        frame.pack()

    def start(self, start_message=None):
        pass

    def get_guess(self, game_digits=None, default_answer=None):
        pass

    def choose_a_mode(self, available_modes=None):
        pass

    def draw_screen(self, current_try=None):
        self.root.mainloop()
