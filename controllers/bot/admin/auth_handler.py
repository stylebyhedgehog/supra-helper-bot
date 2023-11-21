from exceptions.bot_error_handler import bot_error_handler
from services.bot.authentication_service import AuthenticationService
from utils.constants.messages import PAM_AUTH
from utils.logger import Logger


def register_admin_auth_handlers(bot):
    @bot.message_handler(commands=['login_admin'])
    @bot_error_handler(bot)
    def handle_admin_login(message):
        if AuthenticationService.is_admin_authorized(message.chat.id):
            bot.send_message(message.chat.id, PAM_AUTH.ERROR_ALREADY_AUTHENTICATED)
        else:
            admin_password = message.text.split()
            admin_password = admin_password[1]
            username = AuthenticationService.authorize_admin(admin_password, message.chat.id, message.from_user.username)
            if username:
                msg = PAM_AUTH.RESULT(username)
                bot.send_message(message.chat.id, msg)
                Logger.bot_info(message.chat.id,
                                f"location: authentication. Admin with tg_username={username} successfully authenticated")

            else:
                msg = PAM_AUTH.ERROR_WRONG_PASSWORD
                bot.send_message(message.chat.id, msg)
                Logger.bot_handled_error(message.chat.id,
                                         f"location: admin_authentication. Admin with tg_username={username} not authenticated")

