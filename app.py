import logging
from Game import Controller
from Game import IO
from Game import Helper

if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO)
    io = IO()
    helper = Helper()
    c = Controller(io=io, helper=helper)
    c.play()
