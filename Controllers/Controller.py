import sys
#from AbstractClasses.AbstractController import AbstractController
from Model.Game import Game
from time import sleep


class Controller(object):
    def __init__(self, io=None):
        self.io = io
        #super(Controller, self).__init__(io=io)

    def play(self):
        self.io.instructions()
        self.io.construct(callback=self)

        self.io.update_screen()

        # Ask if the user wants to play
        if not self.io.want_to_play():
            # At this point, the user has said they don't want to play. So
            # give a farewell and then return control to app.py.
            self.io.finish("Okay, come back soon!")
            return

        self.io.report_status("Connecting to the game server...")

        # The user has started a game, so ask the Game model to create a new
        # game object; note, no game is started yet, that only happens when
        # a call to game.get_game is made. Also, a callback notifier is
        # passed to enable the object to perform user AbstractIO.
        game = Game(callback_notifier=self.io.report_status)
        sleep(1)

        # Get the Game model to check if the server is ready. It will take
        # configuration from os environment variables. See Game.py for more
        # information.
        if not game.check_game_server_ready():
            # The Game model couldn't reach the server or did not receive
            # a ready response, so report to the user and return control
            # to app.py.
            self.io.report_error(
                "Sorry, the cowbull game isn't available right now; "
                "please come back later. The issue has been logged."
            )
            return
        self.io.report_status("Connected to game server. Fetching available game modes...")
        sleep(1)

        # Ask the Game model to get a list of available modes. The Game
        # servers may have different modes, so the Game model always
        # checks.
        modes, error_detail = game.get_modes()
        sleep(1)

        if not modes:
            # For some reason (contained in the error detail), the modes
            # weren't returned properly; therefore, the game cannot play.
            self.io.report_error(error_detail)
            return()

        available_modes = [str(i['mode']) for i in modes]
        self.io.report_status("Game is ready. Modes available are: {}".format(', '.join(available_modes)))

        # Ask the user to chose a mode to play.
        mode, error_detail = self.io.choose_a_mode(
            available_modes=available_modes
        )
        if not mode:
            # This should never be reachable, but just in case :)
            self.io.report_error(error_detail)
            return()

        self.io.setup(10)

        self.io.draw_screen()

    def instructions(self):
        self.io.instructions()

    def quit(self):
        if self.io.quit():
            sys.exit(0)
