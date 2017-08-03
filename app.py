import logging
from Game import Game
from Game import Helper
from Game import IO


def main():
    io = IO()
    io.instructions()

    if not io.want_to_play():
        print("Okay, come back soon!")
        exit()

    game = Game(io=io, helper=Helper())

    if not game.check_game_server_ready():
        print("Sorry, the cowbull game isn't available right now; "
              "please come back later. The issue has been logged.")
        return

    modes = game.get_modes()
    if not modes:
        exit()

    mode = io.choose_a_mode(game_modes=modes)
    if not mode:
        exit()

    if game.get_game(mode=mode):
        game.play_game()


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO)
    main()
