class Helper(object):
    def __init__(self):
        pass

    def get_input(
            self,
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
        _answer = None

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
