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

    def __init__(self):
        self.game = None
        self.io_controller = None

    def execute(self, game=None, mode=None, io_controller=None):
        self.check_required(game=game, io_controller=io_controller)
        self.game = game
        self.io_controller = io_controller

    @staticmethod
    def check_required(game=None, io_controller=None):
        if not game:
            raise ValueError("Game is not declared and must be passed to execute.")
        if not io_controller:
            raise ValueError("IO Controller is not set. Game cannot be played.")
        if not isinstance(io_controller, AbstractIO):
            raise TypeError("IO Controller is not an instance of AbstractIO")
