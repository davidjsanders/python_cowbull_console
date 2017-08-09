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
            self.io_controller.setup(game_tries=self.game.game_tries, game_digits=self.game.game_digits)

    def make_guess(self):
        input_list = self.io_controller.get_guess(
            game_digits=self.game.game_digits,
            default_answer=self.game.list_of_digits()
        )

        # Pass the numbers guessed by the user to the game model and
        # ask it to take a turn.
        status, turn_output = self.game.take_turn(input_list)
        finished = status in [self.game.WON, self.game.LOST]

        # Check the status of the turn and find out if there was an
        # error, e.g. the user type x, y, z when numbers were expected.
        # If there's an error, show the error details and then continue
        # looping.
        if status == self.game.ERROR:
            print("In Error")
            self.io_controller.report_error(turn_output)
            return

        self.io_controller.update_result(
            line_number=0,
            result=turn_output["outcome"]["analysis"],
            numbers_guessed=input_list,
            finished=finished
        )

        # Check if the user won or lost the game.
        if finished:
            # Regardless of win or loss, the game is over and the message
            # returned by the Game model needs to be delivered to the
            # user. The finish_message is updated and the loop is broken.
            self.io_controller.finish(finish_message=turn_output["outcome"]["message"])
            return
