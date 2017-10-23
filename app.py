import argparse
import logging
import os

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
    parser.add_argument('--server',
                        dest='cowbull_server',
                        default='localhost',
                        type=str,
                        help="The name of the cowbull game server, defaults to localhost"
                        )
    parser.add_argument('--port',
                        dest='cowbull_port',
                        default=5000,
                        type=int,
                        help="The port used to serve the cowbull game server, defaults to 5000"
                        )
    parser.add_argument('--game-version',
                        dest='cowbull_version',
                        default="v1",
                        type=str,
                        help="The cowbull game server version, defaults to v1"
                        )

    args = parser.parse_args()

    # Set the environment variables to the arg values
    # only *IF* they are not already set. If set, env.
    # vars. take priority

    if not os.getenv("cowbull_server", None):
        os.environ["cowbull_server"] = args.cowbull_server

    if not os.getenv("cowbull_port", None):
        os.environ["cowbull_port"] = str(args.cowbull_port)

    if not os.getenv("cowbull_version", None):
        os.environ["cowbull_version"] = args.cowbull_version

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
