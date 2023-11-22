from functools import wraps
import traceback
from utils.logger import Logger


def flask_controller_error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            location = func.__name__
            Logger.flask_controller_unhandled_error(location, e, traceback.format_exc())
            return f"Location: {location}\nError: {e}\nTraceback: {traceback.format_exc()}"

    return wrapper
