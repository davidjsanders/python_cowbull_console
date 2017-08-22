import sys

from AbstractClasses.AbstractController import AbstractController


class GUIController(AbstractController):
    def __init__(self, io_controller=None):
        super(GUIController, self).__init__(io_controller)

    def make_guess(self, line_number=None):
        return super(GUIController, self).make_guess(line_number)

    def play(self):
        return_state = super(GUIController, self).play()
        if return_state == self.SIGNAL_BREAK:
            sys.exit(0)

        if self.game_ready:
            # If we're here, then the game was successfully created and
            # the next step in the console model is to ask the user to
            # choose a mode.
            mode, error_detail = self.io_controller.choose_a_mode(
                available_modes=self.available_modes
            )
            if not mode:
                # This should never be reachable, but just in case :)
                self.io_controller.report_error(error_detail)
                return

            self.io_controller.run_loop()

    #
    # Callback Methods for GUI control
    #

    def play_mode(self, mode=None):
        game_status, error_detail = self.game.get_game(mode=mode)
        if game_status:
            # If we're here, then the game was successfully created; note,
            # this app has no knowledge of the game object or how it was
            # created. If the AbstractView has a start message, tell it to show.
            self.io_controller.start("Okay, the game is about to begin.")

            # Setup the header and screen based on the mode (the number of
            # digits and the number of guesses) of the game.
            self.io_controller.setup(game_tries=self.game.game_tries, game_digits=self.game.game_digits)

    def instructions(self):
        self.io_controller.instructions()

    def quit(self):
        if self.io_controller.quit():
            sys.exit(0)
