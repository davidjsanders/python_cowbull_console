from AbstractClasses.Controller import Controller


class TkController(Controller):
    def __init__(self, io=None):
        super(TkController, self).__init__(io=io)

    def play(self):
        self.io.setup()
        self.io.draw_screen()
