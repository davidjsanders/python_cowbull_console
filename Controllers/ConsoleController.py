from AbstractClasses.AbstractController import AbstractController


class ConsoleController(AbstractController):
    def __init__(self, io_controller=None):
        super(ConsoleController, self).__init__(io_controller)

    def make_guess(self, line_number=None):
        return super(ConsoleController, self).make_guess(line_number=line_number)

    def play(self):
        super(ConsoleController, self).play()

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

            # Now create a game with the requested mode.
            self.game.get_game(mode=mode)

            # If the AbstractView has a start message, tell it to show.
            # Ask the user to chose a mode to execute.
            self.io_controller.start("Okay, the game is about to begin.")

            # Setup the header and screen based on the mode (the number of
            # digits and the number of guesses) of the game.
            self.io_controller.setup(game_tries=self.game.game_tries, game_digits=self.game.game_digits)

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

                if return_signal == self.SIGNAL_FINISH:
                    # Regardless of win or loss, the game is over and the message
                    # returned by the Game model needs to be delivered to the
                    # user. The finish_message is updated and the loop is broken.
                    self.io_controller.draw_screen(current_try=counter)
                    self.io_controller.finish(finish_message=output["outcome"]["status"])
                    break
                elif return_signal == self.SIGNAL_ERROR:
                    continue

                # Increment the guess counter.
                counter += 1

                # Draw the screen
                print("Output: {}".format(output))
                input("Press enter")
                self.io_controller.report_status(message=output["outcome"]["status"])
                self.io_controller.draw_screen(current_try=counter)

                # Check if the user has exceeded their guesses. If they have,
                # break the loop.
                if counter > self.game.game_tries:
                    break
        else:
            # The else block is reached if the Game model is unable to create and
            # initiate a game. This shouldn't happen, but can, so the error is
            # reported and control returns to app.py
            self.io_controller.report_error("An unexpected error has occurred!")
            self.io_controller.report_status(
                message="For some reason, it has not been possible to start the game. Sorry."
            )
