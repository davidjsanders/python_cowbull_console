import json
import logging
import os


class ErrorHandler(object):
    defaults = {}

    def __init__(self, **kwargs):
        self.defaults["module"] = kwargs.get("module", None)
        self.defaults["method"] = kwargs.get("method", None)
        self.basicConfig = logging.basicConfig

    #
    # Properties
    #
    @property
    def module(self):
        return self.defaults["module"]

    @module.setter
    def module(self, value):
        if not isinstance(value, str):
            raise TypeError("Module must be a string.")
        self.defaults["module"] = value

    @property
    def method(self):
        return self.defaults["method"]

    @method.setter
    def method(self, value):
        if not isinstance(value, str):
            raise TypeError("Method must be a string.")
        self.defaults["method"] = value

    #
    # 'public' methods
    #
    def error(self, module=None, method=None, status=None, exception=None, message=None):
        response_dict = {
            "status": status or "NA",
            "module": module or self.defaults["module"],
            "method": method or self.defaults["method"],
            "exception": exception,
            "message": message or "No message was provided!"
        }

        self.log(
            calling_module=response_dict["module"],
            calling_method=response_dict["method"],
            exception=response_dict["exception"],
            status=response_dict["status"],
            message=response_dict["message"],
            logger=logging.error,
            verbose=True
        )

        return {
            "mimetype": "application/json",
            "status": response_dict["status"],
            "response": json.dumps(response_dict)
        }

    def log(
            self,
            calling_module=None,
            calling_method=None,
            exception=None,
            status=None,
            message=None,
            logger=None,
            verbose=None
    ):
        if logger is None:
            logger = logging.debug
        if verbose is None:
            _verbose = os.getenv("debug_verbose", False) == "true"
        else:
            _verbose = verbose

        if _verbose:
            _message = "MODULE:{}({}) STATUS:{} MESSAGE:{} {}".format(
                calling_module or self.defaults["module"],
                calling_method or self.defaults["method"],
                status,
                message,
                "EXCEPTION:{}".format(exception) if exception is not None else ""
            )
        else:
            _message = "{}: {}: {}".format(
                calling_module or self.defaults["module"],
                calling_method or self.defaults["method"],
                message
            )

        logger(_message)
