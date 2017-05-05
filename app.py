import logging
from Game import Game


def setup():
    g = Game()
    g.instructions()

    if g.want_to_play():
        play(g)
    else:
        print("Okay, come back soon!")


def play(game):
    if game.check_ready():
        print("Coming soon")
    else:
        print("Sorry, the cowbull game isn't available right now; "
              "please come back later. The issue has been logged.")
        return




if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=logging.DEBUG)
    setup()
