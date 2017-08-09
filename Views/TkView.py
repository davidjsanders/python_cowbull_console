import sys
from AbstractClasses.AbstractIO import AbstractIO
from AbstractClasses.AbstractController import AbstractController
from Views.TkViewHelpers.TkViewStatusFrame import TkViewStatusFrame

if sys.version_info[0] < 3:
    import Tkinter as Tkinter
    import tkMessageBox as MessageBox
    from Tkinter import *
else:
    import tkinter as Tkinter
    import tkinter.messagebox as MessageBox
    from tkinter import *


class TkView(AbstractIO):
    welcome_msg = "Welcome to the CowBull game. The objective of this game is to guess " \
                  "a set of digits by entering a sequence of numbers. Each time you try " \
                  "to guess, you will see an analysis of your guesses and be given a " \
                  "number of tries to win. Choose a mode to play."

    app_name = "Python Cowbull Console Game"

    def __init__(self):
        super(TkView, self).__init__()
        self.root = None
        self.frame = None
        self.instructions_frame = None
        self.button_frame = None
        self.play_frame = None
        self.status_frame = None
        self._callback = None
        self.menu_bar = None
        self.file_menu = None
        self.file_new_menu = None
        self.help_menu = None

    #
    # Concrete implementations of abstract methods
    # --------------------------------------------

    def construct(self, callback=None):
        if callback:
            self._callback = callback
        self._check_callback(value=self._callback)

        self.root = Tk()
        Grid.rowconfigure(self.root, 0, weight=1, minsize=350)
        Grid.columnconfigure(self.root, 0, weight=1, minsize=500)

        self.frame = Frame(self.root)
        self.frame.grid(row=0, column=0, sticky=N + S + E + W)
        Grid.columnconfigure(self.frame, 0, weight=1)

        #
        # Instructions frame
        #
        self.instructions_frame = LabelFrame(self.frame, text="Instructions")
        instruction_text = Text(self.instructions_frame)
        instruction_text.tag_config("textformat", borderwidth=3, wrap=WORD)
        instruction_text.insert(INSERT, self.welcome_msg, ("textformat"))
        instruction_text.config(
            state=DISABLED,
            height=1,
            font=("Helvetica", 16),
            borderwidth=7
        )
        instruction_text.grid(row=0, column=0, ipadx=10, ipady=5, sticky=N + S + E + W)
        Grid.rowconfigure(self.instructions_frame, 0, weight=0, minsize=100)
        Grid.columnconfigure(self.instructions_frame, 0, weight=1)
        self.instructions_frame.grid(row=0, column=0, padx=0, pady=3, sticky=N + S + E + W)
        Grid.rowconfigure(self.frame, 0, weight=0, minsize=100)

        #
        # Button / control frame
        #
        self.button_frame = LabelFrame(self.frame, text="Game options", padx=2, pady=2)
        self.button_frame.grid(row=1, column=0, sticky=N + S + E + W, padx=0, pady=0)
        Label(
            self.button_frame,
            text=" "
        ).grid(row=0, column=0)
        Grid.rowconfigure(self.frame, 1, weight=0, minsize=60)

        #
        # Play area frame
        #
        self.play_frame = Frame(self.frame, bg="green", padx=10, pady=10)
        self.play_frame.grid(row=2, column=0, sticky=N + S + E + W, padx=0, pady=0)
        Button(self.play_frame).grid(row=0, column=0, sticky=N + S + E + W)
        Grid.rowconfigure(self.frame, 2, weight=1)

        #
        # Status frame
        #
        self.status_frame = TkViewStatusFrame(
            parent=self.frame,
            status="Status frame created.",
            bg="blue",
            padx=0,
            pady=0
        )
        self.status_frame.grid(row=3, column=0, sticky=N + S + E + W, padx=0, pady=0)
        Grid.rowconfigure(self.frame, 3, weight=0, minsize=40)

        #
        # Menu
        #
        self.menu_bar = Menu(self.root)
        self.file_menu = Menu(self.menu_bar)
        self.menu_bar.add_cascade(label="File", underline=1, menu=self.file_menu)

        self.file_new_menu = Menu(self.file_menu)
        self.file_menu.add_cascade(label="New Game", underline=1, menu=self.file_new_menu)

        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self._callback.quit)

        self.help_menu = Menu(self.menu_bar)
        self.menu_bar.add_cascade(label="Help", underline=1, menu=self.help_menu)
        self.help_menu.add_command(label="Instructions", command=self._callback.instructions)

        #
        # Final configuration
        #
        self.root.config(menu=self.menu_bar)
        self.root.update()
        self.root.minsize(500, 750)

    def instructions(self, instruction_text=None, info_text=None, author=None):
        pass

    def report_status(self, message=None):
        self.status_frame.set_text(status=message)
        self.status_frame.update()

    def want_to_play(self):
        self.report_status("Asking for permission to connect to the network.")
        return_status = MessageBox.askyesno(self.app_name, self.network_message)
        return return_status

    def report_error(self, error_detail=None):
        MessageBox.showerror(
            title=TkView.app_name,
            message="An error has occurred: {}".format(error_detail)
        )

    def update_result(self, line_number=None, result=None, numbers_guessed=None):
        pass

    def finish(self, finish_message=None):
        pass

    def setup(self, game_tries=None):
        pass

    def start(self, start_message=None):
        pass

    def get_guess(self, game_digits=None, default_answer=None):
        pass

    def choose_a_mode(self, available_modes=None):
        if not available_modes:
            return None, "The game server returned no modes. Unable to continue playing."
        colcount = 0
        for mode in available_modes:
            Button(
                self.button_frame,
                text=mode.capitalize()
            ).grid(row=0, column=colcount, sticky=E)
            colcount += 1
        Button(
            self.button_frame,
            text="Quit",
            command=self._callback.quit
        ).grid(row=0, column=colcount, sticky=E)
        return available_modes[0], None

    def draw_screen(self, current_try=None):
        self._check_callback(value=self._callback)
        self.root.mainloop()

    def update_screen(self):
        self.root.update()

    #
    # 'Private' methods
    # -----------------

    @staticmethod
    def quit():
        return MessageBox.askyesno(TkView.app_name, "Quit the game?")

    @staticmethod
    def _check_callback(value):
        pass
        #if not value or not isinstance(value, AbstractController):
        #    raise TypeError("Callback must be set and must be a subclass of AbstractClasses.AbstractController")
