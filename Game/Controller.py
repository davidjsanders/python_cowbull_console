from .Game import Game
from .IO import IO
from .Helper import Helper


class Controller(object):
    def __init__(self):
        pass

    def play(self):
        io = IO()
        io.instructions()

        if not io.want_to_play():
            print("Okay, come back soon!")
            exit()

        game = Game(helper=Helper())

        if not game.check_game_server_ready():
            print("Sorry, the cowbull game isn't available right now; "
                  "please come back later. The issue has been logged.")
            return

        modes, error_detail = game.get_modes()
        if not modes:
            io.print_error(error_detail)
            exit()

        mode, error_detail = io.choose_a_mode(game_modes=modes)
        if not mode:
            io.print_error(error_detail)
            exit()

        game_status, error_detail = game.get_game(mode=mode)
        if game_status:
            io.setup_header(game_digits=game.game_digits, game_tries=game.game_tries)
            io.draw_screen()

            finish_message = "Okay, thanks for playing!"

            io.setup_header(game_digits=game.game_digits, game_tries=game.game_tries)
            io.draw_screen()
            counter = 1
            while True:
                input_list = io.get_input(game.game_digits)
                if input_list == [-1]:  # Capture sentinel
                    break

                status, turn_output = game.take_turn(input_list)
                if status == Game.ERROR:
                    io.print_error(turn_output)
                    continue

                io.update_line(
                    lineno=counter,
                    result=turn_output["outcome"]["analysis"],
                    numbers_input=input_list
                )
                io.draw_screen()

                if status in [Game.WON, Game.LOST]:
                    finish_message = turn_output["outcome"]["message"]
                    break

                counter += 1
                if counter > game.game_tries:
                    break

            io.print_finish(finish_message)
        else:
            io.print_error(error_detail)
            io.print_error(error_detail="For some reason, it has not been possible to start the game. Sorry.")

