from db.repositories.administrator_repository import AdministratorRepository
from utils.constants.callback_names import CPP
from utils.constants.messages import PPM_CONTACT


def register_contact_administrator(bot):
    @bot.message_handler(func=lambda message: message.text.lower() == CPP.MENU_CONTACT.lower())
    def contact_administrator_handler(message):
        administrators = AdministratorRepository.find_all_administrators()
        if administrators and len(administrators) > 0:
            admin = administrators[0]
            bot.send_message(message.chat.id, PPM_CONTACT.RESULT(admin.telegram_username))
        else:
            bot.send_message(message.chat.id, PPM_CONTACT.ERROR_ADMIN_NOT_FOUND)
