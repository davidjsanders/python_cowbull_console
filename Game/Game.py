import json
import logging
import os
import requests
from time import sleep
from .Helper import Helper
from .IO import IO


class Game:
    WON = -1
    LOST = -2
    ERROR = -3
    CONTINUE = 0

    def __init__(self, helper=None):
        self.game_server = dict()
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
        self.game_modes = None
        self.guesses = []

        self.helper = helper or Helper()

    def get_modes(self):
        self.game_modes, status = self.helper.get_url_json(
            url=self.modes_url,
            headers={"Content-type": "application/json"},
            retries=3,
            delay_increment=5
        )

        in_error, error_detail = self.helper.check_status(status, self.game_modes)

        if in_error:
            return False, error_detail

        return self.game_modes, None

    def check_game_server_ready(self):
        json_data, status = self.helper.get_url_json(url=self.ready_url, retries=3, delay_increment=5)
        if status == 200 and 'status' in json_data and json_data['status'] == "ready":
            return True
        else:
            return False

    def get_game(self, mode=None):
        if mode is None:
            mode = "normal"

        self.game, status = self.helper.get_url_json(
            url=self.game_url+"?mode={}".format(mode),
            retries=3,
            delay_increment=5
        )

        in_error, error_detail = self.helper.check_status(status, self.game)

        if in_error:
            return False, error_detail

        self.game_key = self.game.get("key", None)
        self.game_digits = int(self.game.get("digits", 0))
        self.game_tries = int(self.game.get("guesses", 0))

        # TODO MUST ADD GAME CHECKING!

        return True, None

    def take_turn(self, guessed_digits=None):
        game_output, status_code = self.helper.post_url_json(
            url=self.game_url,
            headers={"Content-type": "application/json"},
            data={"key": self.game_key, "digits": guessed_digits},
            retries=3,
            delay_increment=5
        )

        in_error, error_detail = self.helper.check_status(status_code, game_output)

        if in_error:
            return Game.ERROR, error_detail

        status = game_output["game"]["status"]
        if status == "won":
            return Game.WON, game_output
        elif status == "lost":
            return Game.LOST, game_output
        else:
            return Game.CONTINUE, game_output

