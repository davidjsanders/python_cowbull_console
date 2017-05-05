import json
import logging
import os
import requests
from time import sleep


class Game:
    welcome_msg = "Welcome to the CowBull game. The objective of this game is to guess " \
                   "a set of four digits (numbers between 0 and 9) by entering a sequence " \
                   "of numbers. Each time you try to guess, you will see an analysis of " \
                   "your guesses: * is a bull (the right number in the right place), - (" \
                   "the right number in the wrong place), x is a miss, and any of the other " \
                   "symbols followed with + means that the number occurs more than once."

    def __init__(self):
        self.host_url = os.getenv("cowbull_host", "localhost")
        self.host_port = os.getenv("cowbull_port", 5000)
        self.host_ver = os.getenv("cowbull_version", "v0_1")
        self.core_url = "http://{}:{}/{}".format(self.host_url, self.host_port, self.host_ver)
        self.game_url = "{}/game".format(self.core_url)
        self.ready_url = "{}/ready".format(self.core_url)
        self.health_url = "{}/health".format(self.core_url)
        self.game = None
        self.game_key = None
        self.game_digits = None
        self.game_tries = None
        self.guesses = []
        self.user_output_header = [
            "Game Analysis: x (miss), * (Bull), - (Cow), " + chr(27) + "[1mbold" + chr(27) + "[0m (multiple)",
            "-" * 78,
            ""
        ]
        self.user_output_try = ""
        self.user_output = []
        self.user_output_footer = [
            "-" * 78,
            ""
        ]

#        self.user_output = [
#            "Game Analysis: x (miss), * (Bull), - (Cow), " + chr(27) + "[1mbold" + chr(27) +"[0m (multiple)",
#            "-"*78,
#            "",
#            "Try | 1| 2| 3| 4|      | Your guesses",
#            "-"*78,
#            "",
#            "",
#            "",
#            "",
#            "",
#            "",
#            "",
#            "",
#            "",
#            "",
#            "-"*78,
#            ""
#        ]
        self.line_format = "  {:2d}| {}     | {}"
        self.output_offset = 5

    def instructions(self):
        print()
        print(self.welcome_msg)
        print()

    def want_to_play(self):
        while True:
            answer = input("Do you want to play? (Yes/No) ")
            if answer.lower() in ['yes', 'y', 'no', 'n']:
                break
        if answer.lower() in ["yes", "y"]:
            return True
        else:
            return False

    def choose_a_mode(self):
        while True:
            answer = input("Do you want to play normal, easy, or hard mode? ")
            if answer.lower() in ["normal", "easy", "hard"]:
                break
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
                    raise ValueError("The cowbull game is not ready: {}.".format(r.status_code))
                return_status = True
                break
            except requests.ConnectionError as ce:
                logging.debug("check_ready: ConnectionError: {}".format(str(ce)))
                print("Connection failed. Re-trying in {} seconds...".format(timeout))
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

        # Setup the header for the correct number of digits required depending
        # upon the game mode.
        digits_needed = \
            " "+str([str(i+1)+"|" for i in range(0, self.game_digits)])\
            .replace('[','')\
                .replace(']','')\
                .replace(',','')\
                .replace("'",'')

        self.user_output_try = "Try |{}      | Your guesses".format(digits_needed)
        self.user_output = []
        for i in range(0, self.game_tries):
            self.user_output.append("  {:2d}|".format(i+1))

        _=os.system('clear')

        self._show_analysis()
        for i in range(0, self.game_tries):
            input_list = self._get_input()
            if not input_list:
                break
            game_output = self._make_guess(input_list)
            self.user_output[i] = self.line_format\
                .format(
                    i+1,
                    self._analyse_results(game_output["outcome"]["analysis"]),
                    str(input_list).replace('[', '').replace(']', '')
                )
            _ = os.system('clear')
            self._show_analysis()
            status = game_output["game"]["status"]
            if status in ["won", "lost"]:
                finish_message = game_output["outcome"]["message"].replace('[','').replace(']','')
                break
        print()
        print("{}".format(finish_message))

    def _show_analysis(self):
        self._print_lines(self.user_output_header)
        self._print_lines(self.user_output_try)
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
                output_string += chr(27) + "[1m"

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

        try:
            r = requests.post(url=self.game_url, json=payload, headers=headers)
            response_data = r.json()
        except Exception as e:
            print(repr(e))

        return response_data

    def _get_input(self):
        return_list = []
        default_answer = [0, 1, 2, 3]

        while True:
            stdin = input(
                "Enter {} digits (0-9) separated by commas or quit {}: "
                    .format(self.game_digits, default_answer)
            )
            if stdin == "":
                return_list = default_answer
                break

            if stdin.lower() == "quit":
                break

            try:
                split_stdin = stdin.split(',')

                if len(split_stdin) != self.game_digits:
                    raise ValueError("Number of digits incorrect")

                list_of_digits = []
                for digit in split_stdin:
                    _digit = int(digit)
                    if _digit < 0 or _digit > 9:
                        raise ValueError("{} is out of range (0-9)".format(_digit))
                    list_of_digits.append(_digit)
                return_list = list_of_digits
                break
            except ValueError as ve:
                print("{}. You must enter exactly {} digits (from 0 to 9), e.g. 1, 0, 7, 9"
                      .format(str(ve), self.game_digits))
            except Exception as e:
                print("Exception! {}".format(repr(e)))

        return return_list
