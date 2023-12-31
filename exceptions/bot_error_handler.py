import inspect
import os
from functools import wraps
import traceback
from telebot.types import Message, CallbackQuery
from utils.logger import Logger


def bot_error_handler(bot, loc=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                chat_id = None
                signature = inspect.signature(func)
                for arg_name, arg in zip(signature.parameters.keys(), args):
                    if arg_name == "message" and isinstance(arg, Message):
                        chat_id = arg.chat.id
                        break
                    elif arg_name == "call" and isinstance(arg, CallbackQuery):
                        chat_id = arg.message.chat.id
                        break

                if chat_id:
                    bot.send_message(chat_id, "Произошла ошибка системы")

                if loc:
                    location = loc + func.__name__
                else:
                    location = func.__name__

                Logger.bot_unhandled_error(chat_id, location, e, traceback.format_exc())
                bot.send_message(os.getenv("DEVELOPER_TG_CHAT_ID"), f"Critical error on using bot in chat with tg_id={chat_id}, location={location}")

        return wrapper

    return decorator


