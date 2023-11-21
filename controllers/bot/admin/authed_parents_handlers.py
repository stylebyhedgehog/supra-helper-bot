from data_storages.db.repositories.parent_repository import ParentRepository
from exceptions.bot_error_handler import bot_error_handler
from utils.constants.callback_names import CAP


def register_authed_parents_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data == CAP.AUTH_PARENT_LIST)
    @bot_error_handler(bot)
    def get_authed_parents(call):
        parents = ParentRepository.find_all()
        res = "Список авторизованных в системе родителей"
        if len(parents) == 0:
            res+= " пуст"
        for parent in parents:
            res += f"\n{parent.name} - {parent.phone_number} - @{parent.telegram_username}"
        bot.send_message(call.message.chat.id, res)
