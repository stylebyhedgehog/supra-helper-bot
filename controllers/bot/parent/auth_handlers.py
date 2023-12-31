from telebot import types

from exceptions.bot_error_handler import bot_error_handler
from services.bot.authentication_service import AuthenticationService
from utils.constants.messages import PPM_AUTH
from utils.logger import Logger
from utils.string_utils import StringUtil


def register_parent_auth_handlers(bot):
    @bot.message_handler(commands=['logout'])
    @bot_error_handler(bot)
    def handle_parent_logout(message):
        res = AuthenticationService.logout_parent(message.chat.id)
        bot.send_message(message.chat.id, "Вы успешно вышли из системы")
        Logger.bot_info(message.chat.id, "authentication",
                        f"Parent logged out. Result: {res}")

    @bot.message_handler(commands=['login'])
    @bot_error_handler(bot)
    def handle_parent_login(message):
        if AuthenticationService.is_parent_with_tg_id_authorized(message.chat.id):
            bot.send_message(message.chat.id, PPM_AUTH.ERROR_ALREADY_AUTHENTICATED)
            Logger.bot_handled_error(message.chat.id, "authentication", "Parent with such tg_id already authed")
        else:
            markup = types.InlineKeyboardMarkup(row_width=1)
            button1 = types.InlineKeyboardButton(PPM_AUTH.BUTTON_AUTH_METHOD_MANUAL_INPUT,
                                                 callback_data='auth_by_input')
            button2 = types.InlineKeyboardButton(PPM_AUTH.BUTTON_AUTH_METHOD_TG_FETCH, callback_data='auth_by_tg')
            markup.add(button1, button2)
            bot.send_message(message.chat.id, PPM_AUTH.INFO_AUTH_METHOD_SELECTION, reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("auth_by"))
    @bot_error_handler(bot)
    def process_auth_type_selection(call):
        if call.data == 'auth_by_input':
            bot.send_message(call.message.chat.id, PPM_AUTH.INFO_AUTH_METHOD_MANUAL_INPUT_HINT)
            bot.register_next_step_handler(call.message, process_auth_contact_input_handler)
        elif call.data == 'auth_by_tg':
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            item = types.KeyboardButton(PPM_AUTH.BUTTON_AUTH_METHOD_TG_FETCH_PROCESS, request_contact=True)
            markup.add(item)
            bot.send_message(call.message.chat.id, PPM_AUTH.INFO_AUTH_METHOD_TG_FETCH_HINT,
                             reply_markup=markup)

    @bot.message_handler(content_types=['contact'])
    @bot_error_handler(bot)
    def process_auth_contact_tg_handler(message):
        contact = message.contact
        phone_number = contact.phone_number
        parent_tg_id = message.chat.id
        username = message.from_user.username
        _process_auth_on_phone_number_introduced(message, parent_tg_id, phone_number, username)

    @bot_error_handler(bot)
    def process_auth_contact_input_handler(message):
        phone_number = message.text
        parent_tg_id = message.chat.id
        username = message.from_user.username
        _process_auth_on_phone_number_introduced(message, parent_tg_id, phone_number, username)

    def _process_auth_on_phone_number_introduced(message, parent_tg_id, phone_number, username):
        if AuthenticationService.is_parent_with_phone_number_authorized(phone_number):
            bot.send_message(message.chat.id, PPM_AUTH.ERROR_PHONE_NUMBER_ALREADY_USED)
            Logger.bot_handled_error(message.chat.id, "authentication",
                                     f"Parent with such phone_number({phone_number}) already authed")
            return
        result = AuthenticationService.authorize_parent(phone_number, parent_tg_id, username)
        if result:
            parent_name, saved_children_names = result
            string_children_names = StringUtil.list_to_string(saved_children_names)
            msg = PPM_AUTH.RESULT(string_children_names)
            bot.send_message(message.chat.id, msg)
            Logger.bot_info(parent_tg_id, "parent_authentication",
                            f"Parent with phone_number={phone_number} and tg_username={username} successfully authenticated")

        else:
            msg = PPM_AUTH.ERROR_AUTH_FAILED
            bot.send_message(message.chat.id, msg)
            Logger.bot_handled_error(parent_tg_id, "parent_authentication",
                                     f"Parent with phone_number={phone_number} and tg_username={username} not authenticated")
