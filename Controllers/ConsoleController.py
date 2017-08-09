from AbstractClasses.AbstractController import AbstractController
from Model.Game import Game


class ConsoleController(AbstractController):
    """ConsoleController is the control module for the python_cowbull_console game. It is
    initiated by app.py and controls a single game interaction."""
    def __init__(self, io=None):
        super(ConsoleController, self).__init__(io=io)

    def play(self):
        """play initiates instructs the ConsoleController to initiate a game"""

        # Show the instructions to the user.
        self.io.instructions()

        # Ask if the user wants to play
        if not self.io.want_to_play():
            # At this point, the user has said they don't want to play. So
            # give a farewell and then return control to app.py.
            self.io.finish("Okay, come back soon!")
            return

        # The user has started a game, so ask the Game model to create a new
        # game.
        game = Game(callback_notifier=self.io.report_status)

        self.io.report_status("Connecting to the game server...")

        # Get the Game model to check if the server is ready. It will take
        # configuration from os environment variables. See Game.py for more
        # information.
        if not game.check_game_server_ready():
            # The Game model couldn't reach the server or did not receive
            # a ready response, so report to the user and return control
            # to app.py.
            self.io.report_status(
                "Sorry, the cowbull game isn't available right now; "
                "please come back later. The issue has been logged."
            )
            return

        # Ask the Game model to get a list of available modes. The Game
        # servers may have different modes, so the Game model always
        # checks.
        modes, error_detail = game.get_modes()
        if not modes:
            # For some reason (contained in the error detail), the modes
            # weren't returned properly; therefore, the game cannot play.
            self.io.report_error(error_detail)
            return()

        # Ask the user to chose a mode to play.
        mode, error_detail = self.io.choose_a_mode(
            available_modes=[str(i['mode']) for i in modes]
        )
        if not mode:
            # This should never be reachable, but just in case :)
            self.io.report_error(error_detail)
            return()

        # Ask the Game model to create a game using the mode selected by
        # the user.
        game_status, error_detail = game.get_game(mode=mode)
        if game_status:
            # If we're here, then the game was successfully created; note,
            # this app has no knowledge of the game object or how it was
            # created. If the AbstractIO has a start message, tell it to show.
            self.io.start("Okay, the game is about to begin.")

            # Initialize a counter to track the number of guesses which have
            # been made on the game. Note, the user can quit out of the game
            # at any point and control then returns to app.py.
            counter = 1

            # Setup the header and screen based on the mode (the number of
            # digits and the number of guesses) of the game.
            self.io.setup(game_tries=game.game_tries)

            # Draw the screen
            self.io.draw_screen(current_try=counter)

            # Set a default finish message.
            finish_message = "Okay, thanks for playing!"

            # Loop, ask the user for their guess, and then analyze the guess
            # using the Game model.
            while True:
                # Get the guesses from the user.
                input_list = self.io.get_guess(
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
                    self.io.report_error(turn_output)
                    continue

                # Update the line on the screen for the analysis of the guess.
                self.io.update_result(
                    line_number=counter,
                    result=turn_output["outcome"]["analysis"],
                    numbers_guessed=input_list
                )

                # Redraw the screen.
                self.io.draw_screen(current_try=counter)

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
            self.io.finish(finish_message)
        else:
            # The else block is reached if the Game model is unable to create and
            # initiate a game. This shouldn't happen, but can, so the error is
            # reported and control returns to app.py
            self.io.report_error(error_detail)
            self.io.report_status(message="For some reason, it has not been possible to start the game. Sorry.")
