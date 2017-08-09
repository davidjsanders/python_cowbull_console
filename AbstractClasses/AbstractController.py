#
# For compatibility with Python 2.x and 3.x, we use a specific means of
# setting up an abstract class. See the stackoverflow question at
#
# https://stackoverflow.com/questions/35673474/
#   using-abc-abcmeta-in-a-way-it-is-compatible-both-with-python-2-7-and-python-3-5
#
# DO NOT MODIFY THE CODE WITHOUT UNDERSTANDING THE IMPACT UPON PYTHON 2.7
#
import abc
from AbstractClasses.AbstractIO import AbstractIO

# Force compatibility with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


class AbstractController(ABC):
    SIGNAL_ERROR = -2
    SIGNAL_BREAK = -1
    SIGNAL_SUCCESS = 0
    SIGNAL_FINISH = 1

    def __init__(self):
        self.game = None
        self.io_controller = None

    def execute(self, game=None, mode=None, io_controller=None):
        self.check_required(game=game, io_controller=io_controller)
        self.game = game
        self.io_controller = io_controller

    @abc.abstractmethod
    def play_mode(self, mode=None):
        game_status, error_detail = self.game.get_game(mode=mode)
        if game_status:
            # If we're here, then the game was successfully created; note,
            # this app has no knowledge of the game object or how it was
            # created. If the AbstractIO has a start message, tell it to show.
            self.io_controller.start("Okay, the game is about to begin.")

            # Setup the header and screen based on the mode (the number of
            # digits and the number of guesses) of the game.
            self.io_controller.setup(game_tries=self.game.game_tries, game_digits=self.game.game_digits)

        # Return results to caller.
        return game_status, error_detail

    @abc.abstractmethod
    def make_guess(self, line_number=None):
        # Get the guesses from the user.
        input_list = self.io_controller.get_guess(
            game_digits=self.game.game_digits,
            default_answer=self.game.list_of_digits()
        )

        # If a sentinel (-1) is returned, then the user typed quit
        # during entering the numbers.
        if input_list == self.SIGNAL_BREAK:  # Capture sentinel
            return self.SIGNAL_BREAK, None

        # Pass the numbers guessed by the user to the game model and
        # ask it to take a turn.
        status, turn_output = self.game.take_turn(input_list)
        finished = status in [self.game.WON, self.game.LOST]

        # Check the status of the turn and find out if there was an
        # error, e.g. the user type x, y, z when numbers were expected.
        # If there's an error, show the error details and then continue
        # looping.
        if status == self.game.ERROR:
            self.io_controller.report_error(turn_output)
            return self.SIGNAL_ERROR, turn_output

        self.io_controller.update_result(
            line_number=line_number,
            result=turn_output["outcome"]["analysis"],
            numbers_guessed=input_list,
            finished=finished
        )

        # Check if the user won or lost the game.
        if finished:
            self.io_controller.finish(finish_message=turn_output["outcome"]["message"])
            return self.SIGNAL_FINISH, turn_output

        return self.SIGNAL_SUCCESS, None

    @staticmethod
    def check_required(game=None, io_controller=None):
        if not game:
            raise ValueError("Game is not declared and must be passed to execute.")
        if not io_controller:
            raise ValueError("IO Controller is not set. Game cannot be played.")
        if not isinstance(io_controller, AbstractIO):
            raise TypeError("IO Controller is not an instance of AbstractIO")
