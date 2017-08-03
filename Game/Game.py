import json
import logging
import os
import requests
from time import sleep
from .Helper import Helper
from .IO import IO


class Game:
    def __init__(self, io=None, helper=None):
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
        self.io = io or IO()

    def get_modes(self):
        self.game_modes, status = self.helper.get_url_json(
            url=self.modes_url,
            headers={"Content-type": "application/json"},
            retries=3,
            delay_increment=5
        )

        in_error, error_detail = self.helper.check_status(status, self.game_modes)

        if in_error:
            self.io.print_error(error_detail)
            return False

        return self.game_modes

    def check_game_server_ready(self):
        jsondata, status = self.helper.get_url_json(url=self.ready_url, retries=3, delay_increment=5)
        if status == 200 and 'status' in jsondata and jsondata['status'] == "ready":
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
            self.io.print_error(error_detail)
            return False

        self.game_key = self.game.get("key", None)
        self.game_digits = int(self.game.get("digits", 0))
        self.game_tries = int(self.game.get("guesses", 0))

        # TODO MUST ADD GAME CHECKING!

        return True

    def play_game(self):
        finish_message = "Okay, thanks for playing!"

        self.io.setup_header(game_digits=self.game_digits, game_tries=self.game_tries)
        self.io.draw_screen()

        counter = 1

        while True:
            input_list = self.io.get_input(self.game_digits)
            if not input_list:
                continue
            elif input_list == [-1]:  # Capture sentinel
                break

            game_output, status_code = self.helper.post_url_json(
                url=self.game_url,
                headers={"Content-type": "application/json"},
                data={"key": self.game_key, "digits": input_list},
                retries=3,
                delay_increment=5
            )

            in_error, error_detail = self.helper.check_status(status_code, game_output)

            if in_error:
                self.io.print_error(error_detail)
                continue

            self.io.update_line(
                lineno=counter,
                result=game_output["outcome"]["analysis"],
                numbers_input=input_list
            )
            self.io.draw_screen()

            status = game_output["game"]["status"]
            if status in ["won", "lost"]:
                finish_message = game_output["outcome"]["message"]
                break

            counter += 1
            if counter > self.game_tries:
                break

        self.io.print_finish(finish_message)
