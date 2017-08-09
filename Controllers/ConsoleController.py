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

        # Ask the Game model to create a game using the mode selected by
        # the user.
        game_status, error_detail = self.game.get_game(mode=mode)
        if game_status:
            # If we're here, then the game was successfully created; note,
            # this app has no knowledge of the game object or how it was
            # created. If the AbstractIO has a start message, tell it to show.
            self.io_controller.start("Okay, the game is about to begin.")

            # Initialize a counter to track the number of guesses which have
            # been made on the game. Note, the user can quit out of the game
            # at any point and control then returns to app.py.
            counter = 1

            # Setup the header and screen based on the mode (the number of
            # digits and the number of guesses) of the game.
            self.io_controller.setup(game_tries=game.game_tries)

            # Draw the screen
            self.io_controller.draw_screen(current_try=counter)

            # Set a default finish message.
            finish_message = "Okay, thanks for playing!"

            # Loop, ask the user for their guess, and then analyze the guess
            # using the Game model.
            while True:
                # Get the guesses from the user.
                input_list = self.io_controller.get_guess(
                    game_digits=game.game_digits,
                    default_answer=game.list_of_digits()
                )

                # If a sentinel (-1) is returned, then the user typed quit
                # during entering the numbers.
                if input_list == [-1]:  # Capture sentinel
                    break

                # Pass the numbers guessed by the user to the game model and
                # ask it to take a turn.
                status, turn_output = game.take_turn(input_list)

                # Check the status of the turn and find out if there was an
                # error, e.g. the user type x, y, z when numbers were expected.
                # If there's an error, show the error details and then continue
                # looping.
                if status == Game.ERROR:
                    self.io_controller.report_error(turn_output)
                    continue

                # Update the line on the screen for the analysis of the guess.
                self.io_controller.update_result(
                    line_number=counter,
                    result=turn_output["outcome"]["analysis"],
                    numbers_guessed=input_list
                )

                # Redraw the screen.
                self.io_controller.draw_screen(current_try=counter)

                # Check if the user won or lost the game.
                if status in [Game.WON, Game.LOST]:
                    # Regardless of win or loss, the game is over and the message
                    # returned by the Game model needs to be delivered to the
                    # user. The finish_message is updated and the loop is broken.
                    finish_message = turn_output["outcome"]["message"]
                    break

                # Increment the guess counter.
                counter += 1

                # Check if the user has exceeded their guesses. If they have,
                # break the loop.
                if counter > game.game_tries:
                    break

            # The game is over. Print the finish message which will be either the
            # default (if a user quit), a win, or a loss message.
            self.io_controller.finish(finish_message)
        else:
            # The else block is reached if the Game model is unable to create and
            # initiate a game. This shouldn't happen, but can, so the error is
            # reported and control returns to app.py
            self.io_controller.report_error(error_detail)
            self.io_controller.report_status(message="For some reason, it has not been possible to start the game. Sorry.")
