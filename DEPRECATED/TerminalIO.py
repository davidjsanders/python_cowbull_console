import os
from textwrap import wrap


class TerminalIO(object):
    """The TerminalIO class controls the input and output for the python_cowbull_console game for
    ANSIView compatible terminals."""

    ESCAPE_CODE = chr(27)
    UNDERLINE_TEXT = ESCAPE_CODE + "[1m"
    BOLD_TEXT = ESCAPE_CODE + "[4m"
    NORMAL_TEXT = ESCAPE_CODE + "[0m"

    welcome_msg = "Welcome to the CowBull game. The objective of this game is to guess " \
                  "a set of digits by entering a sequence of numbers. Each time you try " \
                  "to guess, you will see an analysis of your guesses: * is a bull (the " \
                  "right number in the right place), - (the right number in the wrong " \
                  "place), x is a miss. Any symbol underlined and highlighted in " \
                  + UNDERLINE_TEXT + BOLD_TEXT + "bold" + NORMAL_TEXT + " " + \
                  "means that the number occurs more than once."

    info_msg = "This game is part of a series which shows how an API based game object " \
               "and server can be created, deployed to multiple platforms (bare metal, " \
               "Docker, Kubernetes, Google App Engine, etc.), and accessed with multiple " \
               "clients (web, console, curses, chat-bot, smartphone, etc.). The game is " \
               "not intended to be challenging; rather to demonstrate approach."

    author = "David Sanders, dsanderscanadaNOSPAM@gmail.com"

    def __init__(self):
        # Define the header - note the use of ANSIView escape sequences - and the output structures
        # for presenting (and collecting) user TerminalIO.
        self.user_output_header = [
            "Game Analysis: * (Bull), - (Cow), x (miss), " +
            TerminalIO.UNDERLINE_TEXT + TerminalIO.BOLD_TEXT + "bold" + TerminalIO.NORMAL_TEXT + " (multiple)",
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

        # Five lines are used for headers, so the first 'data' item has an offset of 5.
        self.output_offset = 5

    @staticmethod
    def instructions(instructions_text=None):
        print()

        for line in wrap(instructions_text or TerminalIO.welcome_msg):
            print(line)
        print()

        for line in wrap(TerminalIO.info_msg):
            print(line)
        print()
        print(TerminalIO.author)
        print()

    @staticmethod
    def get_user_input(
            prompt=None,
            default=None,
            choices=None,
            error_text=None,
            help_text=None,
            ignore_case=None,
            allow_empty=None
    ):
        if choices and len(choices) < 2:
            raise ValueError("Can't prompt for input with only one choice!")

        _ignore_case = ignore_case if ignore_case is not None else True
        _allow_empty = allow_empty if allow_empty is not None else False
        _choices = choices
        _error_text = error_text \
            or 'You must choose from a list of choices: {}'.format(', '.join(_choices)) if _choices \
            else 'You must enter a value. Empty responses are not allowed'

        _help_text = help_text or 'Choose one of {}'.format(', '.join(_choices))
        _default = default

        # Build the prompt
        _prompt_a = "{}".format(prompt or "?")
        _prompt_b = "[{}]".format(default) if _default else ""
        _prompt = "{} {}: ".format(_prompt_a, _prompt_b)

        while True:
            _answer = input(_prompt)

            if _answer == '?':
                print(_help_text)
                continue
            elif _answer == '':
                if _default:
                    _answer = default
                    break
                if _allow_empty:
                    break
            elif not _choices:
                break
            else:
                _choices_to_check = _choices
                if _ignore_case:
                    _answer = _answer.lower()
                    _choices_to_check = [str(c).lower() for c in _choices]

                if _answer in _choices_to_check:
                    break

            print(_error_text)

        return _answer

    def want_to_play(self):
        answer = self.get_user_input(
            prompt="Do you want to play?",
            default="yes",
            choices=["y", "ye", "yes", "n", "no"],
            ignore_case=True,
            help_text="You must answer y(es) or n(o) to the question. If you answer yes, "
                      "the game will start; if you answer no, the game will end."
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

    @staticmethod
    def output_message(message=None):
        print(message)

    @staticmethod
    def print_error(error_detail=None):
        _err = error_detail or "No detail on the error was provided."
        print()
        TerminalIO.output_message("An error occurred: {}".format(_err))
        print()

    @staticmethod
    def _print_lines(list_of_lines):
        for line in list_of_lines:
            print(line)

    def draw_screen(self, current_try):
        self.user_output_try = "Try {}; your guesses:".format(current_try)
        _ = os.system('clear')
        self._print_lines(self.user_output_header)
        print(self.user_output_try)
        print('-'*78)
        self._print_lines(self.user_output)
        self._print_lines(self.user_output_footer)

    def update_line(self, line_number, result, numbers_input):
        self.user_output[line_number - 1] = self.line_format \
            .format(
            line_number,
            self._analyse_results(result),
            str(numbers_input).replace('[', '').replace(']', '')
        )

    @staticmethod
    def _analyse_results(game_analysis):
        output_string = ""

        for analysis_record in game_analysis:
            if analysis_record["multiple"]:
                output_string += TerminalIO.UNDERLINE_TEXT + TerminalIO.BOLD_TEXT

            if analysis_record["match"]:
                output_string += "*"
            elif analysis_record["in_word"]:
                output_string += "-"
            else:
                output_string += "x"

            if analysis_record["multiple"]:
                output_string += TerminalIO.NORMAL_TEXT

            output_string += "| "

        return output_string

    def setup_header(self, game_tries):
        # Setup the header for the correct number of digits required depending
        # upon the game mode.
        self.user_output = []
        for i in range(0, game_tries):
            self.user_output.append("  {:2d}|".format(i+1))

    def choose_a_mode(self, game_modes=None):
        default_choice = "normal"
        available_modes = [str(i['mode']) for i in game_modes]

        if not available_modes:
            return False, 'The game server returned no modes. Unable to continue playing.'

        answer = self.get_user_input(
            prompt="What mode of game would you like to play: {}?".format(', '.join(available_modes)),
            default=default_choice,
            choices=available_modes,
            ignore_case=True,
            help_text="The modes are defined by the game server and, typically, are set to "
                      "provide varying options like easy, normal, and hard. These vary the "
                      "number of guesses you are allowed to make and the number of digits "
                      "you're asked to guess. The names of the modes should be self-explanatory; "
                      "however, it is up to the game server, so they could vary widely."
        )

        return answer.lower(), None

    def get_guess(self, game_digits=None, default_answer=None):
        while True:
            user_input = self.get_user_input(
                prompt="Enter {} digits separated by commas or quit".format(game_digits),
                ignore_case=True,
                allow_empty=True,
                default=','.join([str(d) for d in default_answer]),
                help_text="You need to enter {} digits separated by commas.".format(game_digits)
            )

            if user_input.lower() == "quit":
                return_list = [-1]  # Sentinel to signify quit
                break

            try:
                return_list = user_input.replace(" ", "").split(",")

                if len(return_list) != game_digits:
                    raise ValueError("Number of digits incorrect")

                break
            except ValueError as ve:
                print("{}. You must enter exactly {} digits.".format(
                    str(ve), game_digits))
            except Exception as e:
                print("Exception! {}".format(repr(e)))

        return return_list
