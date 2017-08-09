import sys
from Model.Game import Game
from time import sleep


class Controller(object):
    def __init__(self, io_controller=None, game_controller=None):
        if not io_controller:
            raise ValueError("IO Controller must be passed to the controller!")
        if not game_controller:
            raise ValueError("Game Controller must be passed to the controller!")

        self.io_controller = io_controller
        self.game_controller = game_controller
        #super(Controller, self).__init__(io=io)

    def play(self):
        self.io_controller.instructions()
        self.io_controller.construct(callback=self.game_controller)

        self.io_controller.update_screen()

        # Ask if the user wants to execute
        if not self.io_controller.want_to_play():
            # At this point, the user has said they don't want to execute. So
            # give a farewell and then return control to app.py.
            self.io_controller.finish("Okay, come back soon!")
            return

        self.io_controller.report_status("Connecting to the game server...")

        # The user has started a game, so ask the Game model to create a new
        # game object; note, no game is started yet, that only happens when
        # a call to game.get_game is made. Also, a callback notifier is
        # passed to enable the object to perform user AbstractIO.
        game = Game(callback_notifier=self.io_controller.report_status)
        #sleep(1)

        # Get the Game model to check if the server is ready. It will take
        # configuration from os environment variables. See Game.py for more
        # information.
        if not game.check_game_server_ready():
            # The Game model couldn't reach the server or did not receive
            # a ready response, so report to the user and return control
            # to app.py.
            self.io_controller.report_error(
                "Sorry, the cowbull game isn't available right now; "
                "please come back later. The issue has been logged."
            )
            return
        self.io_controller.report_status("Connected to game server. Fetching available game modes...")
        #sleep(1)

        # Ask the Game model to get a list of available modes. The Game
        # servers may have different modes, so the Game model always
        # checks.
        modes, error_detail = game.get_modes()
        #sleep(1)

        if not modes:
            # For some reason (contained in the error detail), the modes
            # weren't returned properly; therefore, the game cannot execute.
            self.io_controller.report_error(error_detail)
            return()

        available_modes = [str(i['mode']) for i in modes]
        self.io_controller.report_status("Game is ready. Modes available are: {}".format(', '.join(available_modes)))

        # Ask the user to chose a mode to execute.
        mode, error_detail = self.io_controller.choose_a_mode(
            available_modes=available_modes
        )
        if not mode:
            # This should never be reachable, but just in case :)
            self.io_controller.report_error(error_detail)
            return()

        self.io_controller.setup(10)
        self.io_controller.draw_screen()
        self.game_controller.execute(game=game, mode=mode, io_controller=self.io_controller)
