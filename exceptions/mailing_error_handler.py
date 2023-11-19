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
            location = kwargs.get('loc', '') or func.__name__
            full_error_info = f"Ошибка при рассылке \n\tlocation: {location}\n\terror: {e}\n\ttraceback: {traceback.format_exc()}"
            Logger.mailing_error(full_error_info)
            bot.send_message(os.getenv("DEVELOPER_TG_CHAT_ID"), full_error_info)

    return wrapper
