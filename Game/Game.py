import json
import logging
import os
import requests
from time import sleep
from .Helper import Helper


class Game:
    welcome_msg = "Welcome to the CowBull game. The objective of this game is to guess " \
                   "a set of digits by entering a sequence of numbers. Each time you try " \
                   "to guess, you will see an analysis of your guesses: * is a bull (the " \
                   "right number in the right place), - (the right number in the wrong " \
                   "place), x is a miss. Any symbol highlighted in bold means that the " \
                   "number occurs more than once."
    game_server = {
        "host": "localhost",
        "port": 5000,
        "version": "v0_1"
    }

    def __init__(self):
        self.game_server["host"] = os.getenv("cowbull_host", "localhost")
        self.game_server["port"] = os.getenv("cowbull_port", 5000)
        self.game_server["version"] = os.getenv("cowbull_version", "v0_1")

        self.core_url = "http://{}:{}/{}".format(
            self.game_server["host"],
            self.game_server["port"],
            self.game_server["version"]
        )

        self.game_url = "{}/game".format(self.core_url)
        self.modes_url = "{}/modes".format(self.core_url)
        self.ready_url = "{}/ready".format(self.core_url)
        self.health_url = "{}/health".format(self.core_url)

        self.game = None
        self.game_key = None
        self.game_digits = None
        self.game_tries = None
        self.guesses = []
        self.user_output_header = [
            "Game Analysis: * (Bull), - (Cow), x (miss), " + chr(27) + "[1m" + chr(27) + "[4mbold" + chr(27) + "[0m (multiple)",
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
        self.helper = Helper()

    def instructions(self):
        print()
        print(self.welcome_msg)
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

    def _get_modes(self):
        return_modes = None

        try:
            logging.debug("get_modes: Connecting to modes URL: {}".format(self.modes_url))
            r = requests.get(url=self.modes_url)
            if r.status_code != 200:
                raise ValueError("The cowbull game on server {} is not ready: {}.".format(self.ready_url, r.status_code))
            game_modes = r.json()
            return_modes = [str(i['mode']) for i in game_modes]
        except Exception as e:
            logging.debug("check_ready: Exception: {}".format(repr(e)))
            raise

        return game_modes, return_modes

    def choose_a_mode(self):
        default_choice = "normal"
        self.game_modes, available_modes = self._get_modes()

        if not available_modes:
            raise ConnectionError('The game server returned no modes. Unable to continue playing.')

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

        return answer.lower()

    def check_ready(self):
        return_status = False
        try_count = 0
        try_limit = 3

        while try_count < try_limit:
            timeout = 5 * (try_count + 1)
            try:
                logging.debug("check_ready: Connecting to readiness URL: {}".format(self.ready_url))
                r = requests.get(url=self.ready_url)
                if r.status_code != 200:
                    raise ValueError("The cowbull game on server {} is not ready: {}.".format(self.ready_url, r.status_code))
                return_status = True
                break
            except requests.ConnectionError as ce:
                logging.debug("check_ready: ConnectionError: {}".format(str(ce)))
                print("Connection to {} failed. Re-trying in {} seconds...".format(self.ready_url, timeout))
            except ValueError as ve:
                logging.debug("check_ready: ConnectionError: {}".format(str(ve)))
                print("{} Re-trying in {} seconds...".format(str(ve), timeout))
            except Exception as e:
                logging.debug("check_ready: Exception: {}".format(repr(e)))
                print("An unexpected error occurred! {}".format(repr(e)))
                break
            sleep(timeout)
            try_count += 1

        return return_status

    def get_game(self, mode=None):
        if mode is None:
            mode = "normal"
        r = None
        try:
            r = requests.get(self.game_url+"?mode={}".format(mode))
        except requests.ConnectionError as ce:
            pass

        try:
            self.game = r.json()
        except requests.ConnectionError as ce:
            pass

        # TODO Error Check return data
        self.game_key = self.game.get("key", None)
        self.game_digits = int(self.game.get("digits", 0))
        self.game_tries = int(self.game.get("guesses", 0))
        game_server = self.game.get("served-by", None)

        print()
        print("Okay, let's start! You have {} guesses to guess {} digits."
              .format(self.game_tries, self.game_digits))
        print("The game was initially served by {}"
              .format(game_server))

    def play_game(self):
        finish_message = "Okay, thanks for playing!"

        _=os.system('clear')
        self._setup_header()
        self._show_analysis()

        counter = 1

        while True:
            input_list = self._get_input()
            if not input_list:
                continue
            elif input_list == [-1]:  # Capture sentinel
                break

            game_output, status_code = self._make_guess(input_list)
            if status_code != 200:
                error_message = "There's a problem with your guess: {}"
                error_detail = "Wow! Something went wrong, but we do not know what! Please try again"

                if 'exception' in game_output:
                    error_detail = game_output["exception"]
                elif 'message' in game_output:
                    error_detail = game_output['message']
                else:
                    error_detail = "Unknown error?!?"

                print(error_message.format(error_detail))
                continue

            self.user_output[counter-1] = self.line_format\
                .format(
                    counter,
                    self._analyse_results(game_output["outcome"]["analysis"]),
                    str(input_list).replace('[', '').replace(']', '')
                )
            _ = os.system('clear')
            self._show_analysis()
            status = game_output["game"]["status"]
            if status in ["won", "lost"]:
                finish_message = game_output["outcome"]["message"]
                break

            counter += 1
            if counter > self.game_tries:
                break

        print()
        print("{}".format(finish_message))
        print()

    def _setup_header(self):
        # Setup the header for the correct number of digits required depending
        # upon the game mode.
        digits_needed = \
            " "+str(self._list_of_string_digits())\
            .replace('[','')\
                .replace(']','')\
                .replace(',','')\
                .replace("'",'')

        self.user_output_try = "Try |{}  | Your guesses".format(digits_needed)
        self.user_output = []
        for i in range(0, self.game_tries):
            self.user_output.append("  {:2d}|".format(i+1))

    def _list_of_digits(self):
        return [i for i in range(0, self.game_digits)]

    def _list_of_string_digits(self):
        return [str(i+1)+"|" for i in range(0, self.game_digits)]

    def _show_analysis(self):
        self._print_lines(self.user_output_header)
        print(self.user_output_try)
        print('-'*78)
        self._print_lines(self.user_output)
        self._print_lines(self.user_output_footer)

    @staticmethod
    def _print_lines(list_of_lines):
        for line in list_of_lines:
            print(line)

    def _analyse_results(self, game_analysis):
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

    def _make_guess(self, digits):
        payload = {
            "key": self.game_key,
            "digits": digits
        }
        headers = {
            "Content-type": "application/json"
        }
        response_data = None

        status_code = 200
        try:
            r = requests.post(url=self.game_url, json=payload, headers=headers)
            status_code = r.status_code
            response_data = r.json()
        except Exception as e:
            print(repr(e))

        return response_data, status_code

    def _get_input(self):
        return_list = []
        default_answer = self._list_of_digits()

        while True:
            stdin = self.helper.get_input(
                prompt="Enter {} digits separated by commas or quit".format(self.game_digits),
                ignore_case=True,
                allow_empty=True,
                default=','.join([str(d) for d in default_answer]),
                help_text="You need to enter {} digits separated by commas.".format(self.game_digits)
            )

            if stdin.lower() == "quit":
                return_list = [-1]  # Sentinel to signify quit
                break

            try:
                return_list = stdin.split(',')

                if len(return_list) != self.game_digits:
                    raise ValueError("Number of digits incorrect")

                break
            except ValueError as ve:
                print("{}. You must enter exactly {} digits.".format(str(ve)))
            except Exception as e:
                print("Exception! {}".format(repr(e)))

        return return_list
