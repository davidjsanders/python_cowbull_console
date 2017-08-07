import logging
from Game.ConsoleController import ConsoleController as Controller
from Game.ANSI import ANSI as IO

# Code block executed if the program is 'run'
if __name__ == "__main__":
    # Configure logging.
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO)

    # Create an Input/Output object
    io = IO()

    # Initiate the controller passing the TerminalIO and Helper objects
    c = Controller(io=io)

    # Play the game
    c.play()
