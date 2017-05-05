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

    game_object = game.get_game()
    if game_object == {}:
        print("Sorry, but for some reason no game object was returned.")
        return

    game_digits = game_object.get("digits", 0)
    game_tries = game_object.get("guesses", 0)
    game_server = game_object.get("server", None)
    print("You have {} guesses to guess {} digits. The game was served by {}"\
          .format(game_tries, game_digits, game_server))


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=logging.DEBUG)
    setup()
