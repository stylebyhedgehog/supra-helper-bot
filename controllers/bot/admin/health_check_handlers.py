from exceptions.bot_error_handler import bot_error_handler
from utils.logger import Logger


def register_health_check_handlers(bot):
    @bot.message_handler(commands=['health_check'])
    @bot_error_handler(bot)
    def health_check(message):
        bot.send_message(message.chat.id, "Бот работает")
        Logger.bot_info(message.chat.id, "health_check", "Health checked")