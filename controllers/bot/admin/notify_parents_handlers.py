from db_func.repositories.parent_repository import ParentRepository
from exceptions.bot_error_handler import bot_error_handler
from utils.constants.callback_names import CAP

def register_notify_parents_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data == CAP.NOTIFY_AUTHED_PARENTS)
    @bot_error_handler(bot)
    def get_message_for_notification(call):
        bot.send_message(call.message.chat.id, "Введите сообщение для рассылки: ")
        bot.register_next_step_handler(call.message, notify_parents)

    def notify_parents(message):
        notification_message = message.text
        parents = ParentRepository.find_all()
        for parent in parents:
            bot.send_message(parent.telegram_id, notification_message)

        bot.send_message(message.chat.id, "Сообщение отправлено всем авторизованным пользователям")
