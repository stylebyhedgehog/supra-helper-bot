from data_storages.db.repositories.administrator_repository import AdministratorRepository
from exceptions.bot_error_handler import bot_error_handler
from utils.constants.callback_names import CPP_MENU
from utils.constants.messages import PPM_CONTACT


def register_contact_administrator_handlers(bot):
    @bot.message_handler(func=lambda message: message.text.lower() == CPP_MENU.CONTACT.lower())
    @bot_error_handler(bot)
    def contact_administrator_handler(message):
        administrators = AdministratorRepository.find_all()
        if administrators and len(administrators) > 0:
            admin = administrators[0]
            bot.send_message(message.chat.id, PPM_CONTACT.RESULT(admin.telegram_username))
        else:
            bot.send_message(message.chat.id, PPM_CONTACT.ERROR_ADMIN_NOT_FOUND)
