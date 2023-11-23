from data_storages.db.repositories.child_repository import ChildRepository
from data_storages.db.repositories.parent_repository import ParentRepository
from exceptions.bot_error_handler import bot_error_handler
from services.api.alfa.customer import CustomerFetcher
from services.bot.authentication_service import AuthenticationService
from utils.constants.messages import PAM_AUTH
from utils.logger import Logger
from utils.string_utils import StringUtil


def register_admin_auth_handlers(bot):
    @bot.message_handler(commands=['login_admin'])
    @bot_error_handler(bot)
    def handle_admin_login(message):
        if AuthenticationService.is_admin_authorized(message.chat.id):
            bot.send_message(message.chat.id, PAM_AUTH.ERROR_ALREADY_AUTHENTICATED)
        else:
            admin_password = message.text.split()
            admin_password = admin_password[1]
            username = AuthenticationService.authorize_admin(admin_password, message.chat.id,
                                                             message.from_user.username)
            if username:
                msg = PAM_AUTH.RESULT(username)
                bot.send_message(message.chat.id, msg)
                Logger.bot_info(message.chat.id, "admin_authentication",
                                f"Admin with tg_username={username} successfully authenticated")

            else:
                msg = PAM_AUTH.ERROR_WRONG_PASSWORD
                bot.send_message(message.chat.id, msg)
                Logger.bot_handled_error(message.chat.id, "admin_authentication",
                                         f"Admin with tg_username={username} not authenticated")

    @bot.message_handler(commands=['super_parent'])
    @bot_error_handler(bot)
    def handle_login_admin_as_super_parent(message):
        parent_children = CustomerFetcher.all()
        saved_children_names = []
        if parent_children:
            parent_name = "Super Parent"
            parent_id = ParentRepository.save(message.chat.id, parent_name, "Super Parent Phone",
                                              message.from_user.username)
            for parent_child in parent_children:
                child_id = parent_child.get("id")
                child_name = parent_child.get("name")
                ChildRepository.save(parent_id, child_id, child_name)
                saved_children_names.append(child_name)
            bot.send_message(message.chat.id,
                             f"Вы успешно авторизовались как Super Parent\nСписок детей:\n{StringUtil.list_to_string(saved_children_names)}")
            bot.send_message(message.chat.id, "/help для доступа к основным командам")