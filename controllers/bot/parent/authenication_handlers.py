from telebot import types


from services.bot.authentication_service import AuthenticationService
from utils.constants.messages import PPM_AUTH, PAM_AUTH
from utils.string_utils import StringUtil


def register_authorization_handlers(bot):
    @bot.message_handler(commands=['admin'])
    def handle_admin_login(message):
        if AuthenticationService.is_admin_authorized(message.chat.id):
            bot.send_message(message.chat.id, PAM_AUTH.ERROR_ALREADY_AUTHENTICATED)
        else:
            admin_password = message.text.split()
            admin_password = admin_password[1]
            username = AuthenticationService.authorize_admin(admin_password, message.chat.id, message.from_user.username)
            if username:
                msg = PAM_AUTH.RESULT(username)
            else:
                msg = PAM_AUTH.ERROR_WRONG_PASSWORD
            bot.send_message(message.chat.id, msg)

    @bot.message_handler(commands=['login'])
    def handle_parent_login(message):
        if AuthenticationService.is_parent_authorized(message.chat.id):
            bot.send_message(message.chat.id, PPM_AUTH.ERROR_ALREADY_AUTHENTICATED)
        else:
            markup = types.InlineKeyboardMarkup(row_width=1)
            button1 = types.InlineKeyboardButton(PPM_AUTH.BUTTON_AUTH_METHOD_MANUAL_INPUT, callback_data='auth_by_input')
            button2 = types.InlineKeyboardButton(PPM_AUTH.BUTTON_AUTH_METHOD_TG_FETCH, callback_data='auth_by_tg')
            markup.add(button1, button2)
            bot.send_message(message.chat.id, PPM_AUTH.INFO_AUTH_METHOD_SELECTION, reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("auth_by"))
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
    def process_auth_contact_tg_handler(message):
        contact = message.contact
        phone_number = contact.phone_number
        parent_tg_id = message.chat.id
        result = AuthenticationService.authorize_parent(phone_number, parent_tg_id)
        if result:
            parent_name, saved_children_names = result
            string_children_names = StringUtil.list_to_string(saved_children_names)
            msg = PPM_AUTH.RESULT(string_children_names)
        else:
            msg = PPM_AUTH.ERROR_AUTH_FAILED
        bot.send_message(message.chat.id, msg)


    def process_auth_contact_input_handler(message):
        phone_number = message.text
        parent_tg_id = message.chat.id
        result = AuthenticationService.authorize_parent(phone_number, parent_tg_id)
        if result:
            parent_name, saved_children_names = result
            string_children_names = StringUtil.list_to_string(saved_children_names)
            msg = PPM_AUTH.RESULT(string_children_names)
        else:
            msg = PPM_AUTH.ERROR_AUTH_FAILED
        bot.send_message(message.chat.id, msg)