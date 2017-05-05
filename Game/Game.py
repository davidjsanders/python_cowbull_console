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
        self.game_digits = None
        self.game_tries = None
        self.guesses = []

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

    def get_game(self):
        r = None
        try:
            r = requests.get(self.game_url)
        except requests.ConnectionError as ce:
            pass

        try:
            self.game = r.json()
        except requests.ConnectionError as ce:
            pass

        # TODO Error Check return data
        self.game_digits = self.game.get("digits", 0)
        self.game_tries = self.game.get("guesses", 0)
        game_server = self.game.get("served-by", None)

        print()
        print("Okay, let's start! You have {} guesses to guess {} digits."
              .format(self.game_tries, self.game_digits))
        print("The game was initially served by {}"
              .format(game_server))

    def play_game(self):
        input_list = self._get_input()

    def _get_input(self):
        return_list = []

        while True:
            stdin = input(
                "Enter {} digits (0-9) separated by commas or quit."
            )
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
                        raise ValueError("Digit out of range (0-9)")
                    list_of_digits.append(_digit)
                return_list = list_of_digits
                break
            except ValueError as ve:
                print("{}. You must enter exactly {} digits (from 0 to 9), e.g. 1, 0, 7, 9"
                      .format(str(ve), self.game_digits))
            except Exception as e:
                print("Exception! {}".format(repr(e)))
