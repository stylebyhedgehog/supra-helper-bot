import inspect
import os
import traceback
from functools import wraps
from telebot.types import Message, CallbackQuery
from utils.logger import Logger


def mailing_error_handler(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        bot = getattr(self, kwargs.get('bot_attr', 'bot'), None)

        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            location = func.__name__
            Logger.mailing_unhandled_error(location, e, traceback.format_exc(), args[0])
            bot.send_message(os.getenv("DEVELOPER_TG_CHAT_ID"), f"Critical error on mailing, location={location}")

    return wrapper
