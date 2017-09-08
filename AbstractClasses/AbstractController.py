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

from AbstractClasses.AbstractView import AbstractView

from Model.Game import Game
from Helpers.ErrorHandler import ErrorHandler
from time import sleep

# Force compatibility with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


class AbstractController(ABC):
    SIGNAL_ERROR = -2
    SIGNAL_BREAK = -1
    SIGNAL_SUCCESS = 0
    SIGNAL_FINISH = 1

    def __init__(self, io_controller=None, delay=None):
        self.handler = ErrorHandler(
            method="__init__",
            module="AbstractController"
        )

        self.handler.log(message="Validating IO Controller")
        self.check_controller_defined(io_controller=io_controller)

        self.handler.log(message="Initializing variables")
        self.available_modes = None
        self.game_ready = False
        self.delay = delay or 0
        self.io_controller = io_controller

        self.handler.log(message="Instantiating Game object")
        self.game = Game(callback_notifier=self.io_controller.report_status)

    #
    # Abstract Methods
    #

    @abc.abstractmethod
    def play(self):
        self.handler.method = "play"

        self.handler.log(message="Playing game")
        self.handler.log(message="Validating IO Controller")

        self.check_controller_defined(io_controller=self.io_controller)

        self.handler.log(message="Show instructions")
        self.io_controller.instructions()

        self.handler.log(message="Construct any IO structures")
        self.io_controller.construct(callback=self)

        self.handler.log(message="Draw the screen")
        self.io_controller.update_screen()

        # Ask if the user wants to execute
        self.handler.log(message="Asking user if they want to play.")
        if not self.io_controller.want_to_play():
            # At this point, the user has said they don't want to execute. So
            # give a farewell and then return control to app.py.
            self.handler.log(message="User did not want to play.")
            self.io_controller.finish("Okay, come back soon!")
            return self.SIGNAL_BREAK

        self.io_controller.report_status("Connecting to the game server...")

        # The user has started a game, so ask the Game model to create a new
        # game object; note, no game is started yet, that only happens when
        # a call to game.get_game is made. Also, a callback notifier is
        # passed to enable the object to perform user AbstractView.
        # game = Game(callback_notifier=self.io_controller.report_status)
        # sleep(self.delay)

        # Get the Game model to check if the server is ready. It will take
        # configuration from os environment variables. See Game.py for more
        # information.
        if not self.game.check_game_server_ready():
            # The Game model couldn't reach the server or did not receive
            # a ready response, so report to the user and return control
            # to app.py.
            self.io_controller.report_error(
                "Sorry, the cowbull game isn't available right now; "
                "please come back later. The issue has been logged."
            )
            return
        self.io_controller.report_status("Connected to game server. Fetching available game modes...")
        sleep(self.delay)

        # Ask the Game model to get a list of available modes. The Game
        # servers may have different modes, so the Game model always
        # checks.
        modes, error_detail = self.game.get_modes()
        sleep(self.delay)

        if not modes:
            # For some reason (contained in the error detail), the modes
            # weren't returned properly; therefore, the game cannot execute.
            self.io_controller.report_error(error_detail)
            return

        self.available_modes = [str(i['mode']) for i in modes]
        self.io_controller.report_status(
            "{} ready; modes available are: {}".format(
                self.game.game_server["host"],
                ', '.join(self.available_modes)
            )
        )
        self.game_ready = True

    @abc.abstractmethod
    def make_guess(self, line_number=None):
        self.check_controller_defined(io_controller=self.io_controller)
        self.check_game_in_play()

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

        served_by = None
        if 'served-by' in turn_output:
            served_by = turn_output["served-by"]

        self.io_controller.report_status(
            message="{}: Your guess analysis is above".format(served_by)
        )

        self.io_controller.update_result(
            line_number=line_number,
            result=turn_output["outcome"]["analysis"],
            numbers_guessed=input_list,
            finished=finished
        )

        # Check if the user won or lost the game.
        if finished:
            self.io_controller.finish(
                finish_message="{}".format(turn_output["outcome"]["status"])
            )
            return self.SIGNAL_FINISH, turn_output

        return self.SIGNAL_SUCCESS, turn_output


    #
    # Static Methods
    #

    @staticmethod
    def check_controller_defined(io_controller=None):
        if not io_controller:
            raise ValueError("IO Controller is not set. Game cannot be played.")
        if not isinstance(io_controller, AbstractView):
            raise TypeError("IO Controller is not an instance of AbstractView")

    def check_game_in_play(self):
        if not self.game:
            raise ValueError("Game has not been instantiated!")