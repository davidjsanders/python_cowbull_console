import logging
from Game.Controller import Controller


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO)
    c = Controller()
    c.play()
