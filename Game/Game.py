import json
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
        self.core_url = "http://{}:{}/{}/".format(self.host_url, self.host_port, self.host_ver)
        self.game_url = "{}/game".format(self.core_url)
        self.ready_url = "{}/ready".format(self.core_url)
        self.health_url = "{}/health".format(self.core_url)

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
            try:
                r = requests.post(url=self.ready_url)
                if r.status_code != 200:
                    raise ValueError("The cowbull game is not ready: {}.".format(r.status_code))
                return_status = True
                break
            except requests.ConnectionError as ce:
                print("Connection failed. Re-trying in {} seconds...".format(5 * (try_count + 1)))
            except ValueError as ve:
                print("{} Re-trying in {} seconds...".format(str(ve), 5 * (try_count + 1)))
            except Exception as e:
                print()
                print("An unexpected error occurred! {}".format(repr(e)))
                break
            sleep(5 * (try_count + 1))
            try_count += 1

        return return_status

    def get_game(self):
        try:
            pass
        except requests.ConnectionError as ce:
            pass
