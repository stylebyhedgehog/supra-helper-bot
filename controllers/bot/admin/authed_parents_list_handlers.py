from db.repositories.parent_repository import ParentRepository
from utils.constants.callback_names import CAP


def register_get_authed_parents_list(bot):
    @bot.callback_query_handler(func=lambda call: call.data == CAP.AUTH_PARENT_LIST)
    def authed_parents_list_handler(call):
        parents = ParentRepository.find_all_parents()
        res = "Список авторизованных в системе родителей"
        if len(parents) == 0:
            res+= " пуст"
        for parent in parents:
            res += f"\n{parent.name}"
        bot.send_message(call.message.chat.id, res)
