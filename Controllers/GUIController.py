import sys
from AbstractClasses.AbstractController import AbstractController


class GUIController(AbstractController):
    def __init__(self):
        super(GUIController, self).__init__()

    def execute(self, game=None, mode=None, io_controller=None):
        super(GUIController, self).execute(game, mode, io_controller)
        self.io_controller.run_loop()

    def instructions(self):
        self.io_controller.instructions()

    def quit(self):
        if self.io_controller.quit():
            sys.exit(0)

    def play_mode(self, mode=None):
        super(GUIController, self).play_mode(mode=mode)

    def make_guess(self):
        super(GUIController, self).make_guess()
