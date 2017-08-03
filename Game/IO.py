import os
from .Helper import Helper


class IO(object):
    welcome_msg = "Welcome to the CowBull game. The objective of this game is to guess " \
                   "a set of digits by entering a sequence of numbers. Each time you try " \
                   "to guess, you will see an analysis of your guesses: * is a bull (the " \
                   "right number in the right place), - (the right number in the wrong " \
                   "place), x is a miss. Any symbol highlighted in bold means that the " \
                   "number occurs more than once."

    def __init__(self):
        self.helper = Helper()
        self.user_output_header = [
            "Game Analysis: * (Bull), - (Cow), x (miss), " +
            chr(27) + "[1m" + chr(27) + "[4mbold" + chr(27) + "[0m (multiple)",
            "-" * 78,
            ""
        ]
        self.user_output_try = ""
        self.user_output = []
        self.user_output_footer = [
            "-" * 78,
            ""
        ]
        self.line_format = "  {:2d}| {} | {}"
        self.output_offset = 5

    @staticmethod
    def instructions():
        print()
        print(IO.welcome_msg)
        print()

    def want_to_play(self):
        answer = self.helper.get_input(
            prompt="Do you want to play?",
            default="yes",
            choices=["y", "ye", "yes", "n", "no"],
            ignore_case=True,
            help_text="You must answer y(es) or n(o) to the question. If you answer yes, "
                      "the game will start; if you answer no, it will quit."
        )
        if answer in ["yes", "ye", "y"]:
            return True
        else:
            return False

    @staticmethod
    def print_finish(finish_message=None):
        print()
        print("{}".format(finish_message))
        print()

    def draw_screen(self):
        _ = os.system('clear')
        self.show_analysis()

    def update_line(self, lineno, result, numbers_input):
        self.user_output[lineno-1] = self.line_format \
            .format(
            lineno,
            self._analyse_results(result),
            str(numbers_input).replace('[', '').replace(']', '')
        )

    @staticmethod
    def _analyse_results(game_analysis):
        output_string = ""

        for analysis_record in game_analysis:
            if analysis_record["multiple"]:
                output_string += chr(27) + "[1m" + chr(27) + "[4m"

            if analysis_record["match"]:
                output_string += "*"
            elif analysis_record["in_word"]:
                output_string += "-"
            else:
                output_string += "x"

            if analysis_record["multiple"]:
                output_string += chr(27) + "[0m"

            output_string += "| "

        return output_string

    def setup_header(self, game_digits, game_tries):
        # Setup the header for the correct number of digits required depending
        # upon the game mode.
        digits_needed = \
            " "+str(self.helper.list_of_string_digits(game_digits))\
            .replace('[', '')\
            .replace(']', '')\
            .replace(',', '')\
            .replace("'", '')

        self.user_output_try = "Try |{}  | Your guesses".format(digits_needed)
        self.user_output = []
        for i in range(0, game_tries):
            self.user_output.append("  {:2d}|".format(i+1))

    def choose_a_mode(self, game_modes=None):
        default_choice = "normal"
        available_modes = [str(i['mode']) for i in game_modes]

        if not available_modes:
            return False, 'The game server returned no modes. Unable to continue playing.'

        answer = self.helper.get_input(
            prompt="What mode of game would you like to play: {}?".format(', '.join(available_modes)),
            default=default_choice,
            choices=available_modes,
            ignore_case=True,
            help_text="The modes are defined by the game server and, typically, are set to "
                      "provide varying options like easy, normal, and hard. These vary the "
                      "number of guesses you are allowed to make and the number of digits "
                      "you're asked to guess. The names of the modes should be self-explanatory."
        )

        return answer.lower(), None

    @staticmethod
    def print_error(error_detail=None):
        _err = error_detail or "No detail on the error was provided."

        print()
        print("An error occurred: {}".format(_err))
        print()

    @staticmethod
    def print_lines(list_of_lines):
        for line in list_of_lines:
            print(line)

    def get_input(self, game_digits=None):
        default_answer = self.helper.list_of_digits(game_digits)

        while True:
            stdin = self.helper.get_input(
                prompt="Enter {} digits separated by commas or quit".format(game_digits),
                ignore_case=True,
                allow_empty=True,
                default=','.join([str(d) for d in default_answer]),
                help_text="You need to enter {} digits separated by commas.".format(game_digits)
            )

            if stdin.lower() == "quit":
                return_list = [-1]  # Sentinel to signify quit
                break

            try:
                return_list = stdin.replace(" ", "").split(",")

                if len(return_list) != game_digits:
                    raise ValueError("Number of digits incorrect")

                break
            except ValueError as ve:
                print("{}. You must enter exactly {} digits.".format(
                    str(ve), len(self.helper.list_of_digits(game_digits))))
            except Exception as e:
                print("Exception! {}".format(repr(e)))

        return return_list

    def show_analysis(self):
        self.print_lines(self.user_output_header)
        print(self.user_output_try)
        print('-'*78)
        self.print_lines(self.user_output)
        self.print_lines(self.user_output_footer)
