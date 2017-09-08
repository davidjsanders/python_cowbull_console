import logging
import os
import requests
from time import sleep


class Game:
    WON = -1
    LOST = -2
    ERROR = -3
    CONTINUE = 0

    def __init__(self, callback_notifier=None):
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
        self.instructions = None
        self.notes = None
        self.default_mode = None
        self._callback_notifier = callback_notifier

    @property
    def callback_notifier(self):
        return self._callback_notifier

    @callback_notifier.setter
    def callback_notifier(self, value):
        self._callback_notifier = value

    def get_modes(self):
        _mode_info, status = self.get_url_json(
            url=self.modes_url,
            headers={"Content-type": "application/json"},
            retries=3,
            delay_increment=5
        )

        in_error, error_detail = self.check_status(status, _mode_info)

        if in_error:
            return False, error_detail

        self.game_modes = _mode_info.get("modes", [])
        self.instructions = _mode_info.get("instructions", "")
        self.notes = _mode_info.get("notes","")
        self.default_mode = _mode_info.get("default_mode", None)

        return self.game_modes, None

    def check_game_server_ready(self):
        json_data, status = self.get_url_json(
            url=self.ready_url,
            retries=3,
            delay_increment=5
        )
        if status == 200 and 'status' in json_data and json_data['status'] == "ready":
            return True
        else:
            return False

    def get_game(self, mode=None):
        if mode is None:
            mode = "normal"

        self.game, status = self.get_url_json(
            url=self.game_url+"?mode={}".format(mode),
            retries=3,
            delay_increment=5
        )

        in_error, error_detail = self.check_status(status, self.game)

        if in_error:
            return False, error_detail

        self.game_key = self.game.get("key", None)
        self.game_digits = int(self.game.get("digits", 0))
        self.game_tries = int(self.game.get("guesses", 0))

        # TODO MUST ADD GAME CHECKING!

        return True, None

    def take_turn(self, guessed_digits=None):
        game_output, status_code = self.post_url_json(
            url=self.game_url,
            headers={"Content-type": "application/json"},
            data={"key": self.game_key, "digits": guessed_digits},
            retries=3,
            delay_increment=5
        )

        in_error, error_detail = self.check_status(status_code, game_output)

        if in_error:
            return Game.ERROR, error_detail

        status = game_output["game"]["status"]
        if status == "won":
            return Game.WON, game_output
        elif status == "lost":
            return Game.LOST, game_output
        else:
            return Game.CONTINUE, game_output

    def list_of_digits(self):
        return [i for i in range(0, self.game_digits)]

    def list_of_string_digits(self):
        return [str(i+1)+"|" for i in range(0, self.game_digits)]

    def get_url_json(
            self,
            url=None,
            headers=None,
            retries=None,
            delay_increment=None
    ):
        if url is None:
            raise ValueError("The URL cannot be empty")

        if not retries:
            try_limit = 5
        else:
            try_limit = retries

        if not delay_increment:
            _delay = 5
        else:
            _delay = delay_increment

        return_status = 500
        return_data = {}

        try_count = 0

        while try_count < try_limit:
            timeout = _delay * (try_count + 1)
            try:
                logging.debug("check_game_server_ready: Connecting to readiness URL: {}".format(url))
                r = requests.get(url=url, headers=headers)
                return_status = r.status_code
                if return_status != 200:
                    return_data = {"error": "The URL ({}) returned {} --> {}".format(url, r.status_code, r.text)}
                    break
                return_data = r.json()
                break
            except requests.ConnectionError as ce:
                logging.debug("check_game_server_ready: ConnectionError: {}".format(str(ce)))
                if self._callback_notifier:
                    self._callback_notifier("Connection to {} failed. Re-trying in {} seconds...".format(url, timeout))
            except ValueError as ve:
                logging.debug("check_game_server_ready: ConnectionError: {}".format(str(ve)))
                if self._callback_notifier:
                    self._callback_notifier("{} Re-trying in {} seconds...".format(str(ve), timeout))
            except Exception as e:
                logging.debug("check_game_server_ready: Exception: {}".format(repr(e)))
                if self._callback_notifier:
                    self._callback_notifier("An unexpected error occurred! {}".format(repr(e)))
                return_data = {"error": "An unexpected error occurred accessing {}! {}".format(url, repr(e))}
                break

            sleep(timeout)
            try_count += 1

        return return_data, return_status

    def post_url_json(
            self,
            url=None,
            headers=None,
            data=None,
            retries=None,
            delay_increment=None
    ):
        if url is None:
            raise ValueError("The URL cannot be empty")

        if not isinstance(headers, dict):
            raise TypeError('post_url_json: headers must be a dict of key value pairs.')

        if data and not isinstance(data, dict):
            raise TypeError('post_url_json: data must be provided as an object (dict)')

        if not retries:
            try_limit = 5
        else:
            try_limit = retries

        if not delay_increment:
            _delay = 5
        else:
            _delay = delay_increment

        return_status = 500
        return_data = {}

        try_count = 0

        while try_count < try_limit:
            timeout = _delay * (try_count + 1)
            try:
                logging.debug("check_game_server_ready: Connecting to readiness URL: {}".format(url))
                r = requests.post(url=url, json=data, headers=headers)
                return_status = r.status_code
                if return_status != 200:
                    try:
                        _json = r.json()
                        return_data = _json
                    except Exception:
                        return_data = {"error": "The URL ({}) returned {} --> {}".format(url, r.status_code, r.text)}
                    break
                return_data = r.json()
                break
            except requests.ConnectionError as ce:
                logging.debug("check_game_server_ready: ConnectionError: {}".format(str(ce)))
                if self._callback_notifier:
                    self._callback_notifier("Connection to {} failed. Re-trying in {} seconds...".format(url, timeout))
            except ValueError as ve:
                logging.debug("check_game_server_ready: ConnectionError: {}".format(str(ve)))
                if self._callback_notifier:
                    self._callback_notifier("{} Re-trying in {} seconds...".format(str(ve), timeout))
            except Exception as e:
                logging.debug("check_game_server_ready: Exception: {}".format(repr(e)))
                if self._callback_notifier:
                    self._callback_notifier("An unexpected error occurred! {}".format(repr(e)))
                return_data = {"error": "An unexpected error occurred accessing {}! {}".format(url, repr(e))}
                break

            sleep(timeout)
            try_count += 1

        return return_data, return_status

    @staticmethod
    def check_status(
            status_code=None,
            dataset=None
    ):
        if not status_code:
            return True, None

        if status_code != 200:
            if not dataset:
                return True, "Wow! Something went wrong, but we do not know what! Please try again"

            if 'exception' in dataset:
                error_detail = dataset["exception"]
            elif 'message' in dataset:
                error_detail = dataset['message']
            elif 'error' in dataset:
                error_detail = dataset["error"]
            else:
                error_detail = "Wow! Something went wrong, but we do not know what! Please try again"

            return True, error_detail

        return False, None
