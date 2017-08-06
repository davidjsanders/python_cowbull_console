import logging
import requests
from time import sleep


class Helper(object):
    def __init__(self):
        pass

    @staticmethod
    def get_input(
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

    @staticmethod
    def get_url_json(
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
                print("Connection to {} failed. Re-trying in {} seconds...".format(url, timeout))
            except ValueError as ve:
                logging.debug("check_game_server_ready: ConnectionError: {}".format(str(ve)))
                print("{} Re-trying in {} seconds...".format(str(ve), timeout))
            except Exception as e:
                logging.debug("check_game_server_ready: Exception: {}".format(repr(e)))
                print("An unexpected error occurred! {}".format(repr(e)))
                return_data = {"error": "An unexpected error occurred accessing {}! {}".format(url, repr(e))}
                break

            sleep(timeout)
            try_count += 1

        return return_data, return_status

    @staticmethod
    def post_url_json(
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
                print("Connection to {} failed. Re-trying in {} seconds...".format(url, timeout))
            except ValueError as ve:
                logging.debug("check_game_server_ready: ConnectionError: {}".format(str(ve)))
                print("{} Re-trying in {} seconds...".format(str(ve), timeout))
            except Exception as e:
                logging.debug("check_game_server_ready: Exception: {}".format(repr(e)))
                print("An unexpected error occurred! {}".format(repr(e)))
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

    @staticmethod
    def list_of_digits(game_digits=None):
        return [i for i in range(0, game_digits)]

    @staticmethod
    def list_of_string_digits(game_digits=None):
        return [str(i+1)+"|" for i in range(0, game_digits)]

