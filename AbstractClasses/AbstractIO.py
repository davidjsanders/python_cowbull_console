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

# Force compatibility with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


class AbstractIO(ABC):
    info_msg = "This game is part of a series which shows how an API based game object " \
               "and server can be created, deployed to multiple platforms (bare metal, " \
               "Docker, Kubernetes, Google App Engine, etc.), and accessed with multiple " \
               "clients (web, console, curses, chat-bot, smartphone, etc.). The game is " \
               "not intended to be challenging; rather to demonstrate approach."

    network_message = "The game is about access the network " \
                      "to connect to the game server; do you want to proceed?"

    author = "David Sanders, dsanderscanadaNOSPAM@gmail.com"

    def __init__(self):
        pass

    @abc.abstractmethod
    def construct(self, callback=None):
        """Construct any required IO features (e.g. GUI or Curses)"""
        pass

    @abc.abstractmethod
    def instructions(self, instruction_text=None, info_text=None, author=None):
        """Show instructions to the user on how to play the game"""
        pass

    @abc.abstractmethod
    def want_to_play(self):
        """Confirm with the user they want to start a game"""
        pass

    @abc.abstractmethod
    def choose_a_mode(self, available_modes=None):
        """Present the user with a list of modes and ask the user to select one"""
        pass

    @abc.abstractmethod
    def setup(self, game_tries=None):
        pass

    @abc.abstractmethod
    def start(self, start_message=None):
        """Display a message at the start of the game"""
        pass

    @abc.abstractmethod
    def draw_screen(self, current_try=None):
        pass

    @abc.abstractmethod
    def finish(self, finish_message=None):
        """Display a message upon completion of the game"""
        pass

    @abc.abstractmethod
    def report_error(self, error_detail=None):
        """Report an error condition to the user"""
        pass

    @abc.abstractmethod
    def report_status(self, message=None):
        """Report an update on status to the user"""
        pass

    @abc.abstractmethod
    def get_guess(self, game_digits=None, default_answer=None):
        """Get the required number of digits (of the correct type) from the user"""
        pass

    @abc.abstractmethod
    def update_result(self, line_number=None, result=None, numbers_guessed=None):
        """Update the output for the user"""
        pass

    @abc.abstractmethod
    def update_screen(self):
        """Force the screen to redraw"""
        pass
