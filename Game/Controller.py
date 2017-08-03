from .Game import Game
from .IO import IO
from .Helper import Helper


class Controller(object):
    def __init__(self, io=None, helper=None):
        self.io = io or IO()
        self.helper = helper or Helper()

    def play(self):
        self.io.instructions()

        if not self.io.want_to_play():
            print("Okay, come back soon!")
            exit()

        game = Game(helper=self.helper)

        if not game.check_game_server_ready():
            print("Sorry, the cowbull game isn't available right now; "
                  "please come back later. The issue has been logged.")
            return

        modes, error_detail = game.get_modes()
        if not modes:
            self.io.print_error(error_detail)
            exit()

        mode, error_detail = self.io.choose_a_mode(game_modes=modes)
        if not mode:
            self.io.print_error(error_detail)
            exit()

        game_status, error_detail = game.get_game(mode=mode)
        if game_status:
            self.io.setup_header(game_digits=game.game_digits, game_tries=game.game_tries)
            self.io.draw_screen()

            finish_message = "Okay, thanks for playing!"

            self.io.setup_header(game_digits=game.game_digits, game_tries=game.game_tries)
            self.io.draw_screen()
            counter = 1
            while True:
                input_list = self.io.get_input(game.game_digits)
                if input_list == [-1]:  # Capture sentinel
                    break

                status, turn_output = game.take_turn(input_list)
                if status == Game.ERROR:
                    self.io.print_error(turn_output)
                    continue

                self.io.update_line(
                    lineno=counter,
                    result=turn_output["outcome"]["analysis"],
                    numbers_input=input_list
                )
                self.io.draw_screen()

                if status in [Game.WON, Game.LOST]:
                    finish_message = turn_output["outcome"]["message"]
                    break

                counter += 1
                if counter > game.game_tries:
                    break

            self.io.print_finish(finish_message)
        else:
            self.io.print_error(error_detail)
            self.io.print_error(error_detail="For some reason, it has not been possible to start the game. Sorry.")
