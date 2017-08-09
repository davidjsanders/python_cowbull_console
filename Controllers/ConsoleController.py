from AbstractClasses.AbstractController import AbstractController
from Model.Game import Game


class ConsoleController(AbstractController):
    """ConsoleController is the control module for the python_cowbull_console game. It is
    initiated by app.py and controls a single game interaction."""
    def __init__(self):
        super(ConsoleController, self).__init__()
        self.game = None
        self.io_controller = None

    def execute(self, game=None, mode=None, io_controller=None):
        super(ConsoleController, self).execute(game=game, mode=mode, io_controller=io_controller)
        self.play_mode(mode=mode)

    def play_mode(self, mode=None):
        game_status, error_detail = super(ConsoleController, self).play_mode(mode=mode)

        # Ask the Game model to create a game using the mode selected by
        # the user.
        if game_status:
            # Initialize a counter to track the number of guesses which have
            # been made on the game. Note, the user can quit out of the game
            # at any point and control then returns to app.py.
            counter = 1

            # Draw the screen
            self.io_controller.draw_screen(current_try=counter)

            # Set a default finish message.
            finish_message = "Okay, thanks for playing!"

            # Loop, ask the user for their guess, and then analyze the guess
            # using the Game model.
            while True:
                return_signal, output = self.make_guess(line_number=counter)
                if return_signal == self.SIGNAL_BREAK:
                    break

                # Increment the guess counter.
                counter += 1

                # Draw the screen
                self.io_controller.draw_screen(current_try=counter)

                if return_signal == self.SIGNAL_FINISH:
                    # Regardless of win or loss, the game is over and the message
                    # returned by the Game model needs to be delivered to the
                    # user. The finish_message is updated and the loop is broken.
                    self.io_controller.finish(finish_message=output["outcome"]["message"])
                    break
                elif return_signal == self.SIGNAL_ERROR:
                    continue

                # Check if the user has exceeded their guesses. If they have,
                # break the loop.
                if counter > self.game.game_tries:
                    break
        else:
            # The else block is reached if the Game model is unable to create and
            # initiate a game. This shouldn't happen, but can, so the error is
            # reported and control returns to app.py
            self.io_controller.report_error(error_detail)
            self.io_controller.report_status(message="For some reason, it has not been possible to start the game. Sorry.")

    def make_guess(self, line_number=None):
        return super(ConsoleController, self).make_guess(line_number=line_number)
