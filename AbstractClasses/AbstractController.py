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


class AbstractController(ABC):

    def __init__(self, io=None):
        if not io:
            raise ValueError("No user input/output control was passed to the ConsoleController!")
        self.io = io

    @abc.abstractmethod
    def play(self):
        pass
