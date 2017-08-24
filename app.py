import logging
import argparse

# Code block executed if the program is 'run'
if __name__ == "__main__":
    # Extract any arguments passed to the app
    parser = argparse.ArgumentParser()
    parser.add_argument('--gui',
                        dest='usegui',
                        default=False,
                        action='store_true',
                        help="Use the GUI interface to the game")
    parser.add_argument('--debug',
                        dest='debugon',
                        default=False,
                        action='store_true',
                        help="Enable debugging.")
    parser.add_argument('--log-format',
                        dest='logformat',
                        type=str,
                        default="%(asctime)s %(levelname)s: %(message)s",
                        help="Set the Python logging format")

    args = parser.parse_args()

    # Decide if using ANSI or GUI
    if args.usegui:
        from Views.TkView import TkView as IO
        from Controllers.GUIController import GUIController as GameController
    else:
        from Views.ConsoleView import ConsoleView as IO
        from Controllers.ConsoleController import ConsoleController as GameController

    # Configure logging.
    if args.debugon:
        logging.basicConfig(format=args.logformat, level=logging.DEBUG)
    else:
        logging.basicConfig(format=args.logformat, level=logging.INFO)

    # Create an Input/Output object
    io = IO()

    # Initiate the controller passing the TerminalIO and Helper objects
    c = GameController(io_controller=io)

    # Play the game
    c.play()
