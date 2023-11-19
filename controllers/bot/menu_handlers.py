import os

from telebot import types

from exceptions.bot_error_handler import bot_error_handler
from services.bot.authentication_service import AuthenticationService
from utils.constants.callback_names import CAP, CPP_MENU
from utils.constants.messages import PPM_MENU, PAM_MENU


def register_menu_handlers(bot):
    @bot.message_handler(commands=['start', 'help'])
    @bot_error_handler(bot)
    def handle_help_parent(message):
        if AuthenticationService.is_parent_authorized(message.chat.id):
            bot.send_message(message.chat.id, PPM_MENU.INFO_POST_AUTH, reply_markup=parent_menu())
        else:
            bot.send_message(message.chat.id, PPM_MENU.INFO_PRE_AUTH)

    @bot.message_handler(commands=['help_admin'])
    @bot_error_handler(bot)
    def handle_help_admin(message):
        if AuthenticationService.is_admin_authorized(message.chat.id):
            admin_menu(bot, message)
        else:
            bot.send_message(message.chat.id, PAM_MENU.INFO_PRE_AUTH)




def parent_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for row in CPP_MENU.MENU:
        markup.add(*[types.KeyboardButton(button) for button in row])
    return markup


def admin_menu(bot, message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for button_info in CAP.menu:
        button = types.InlineKeyboardButton(button_info['text'], callback_data=button_info['callback_data'])
        markup.add(button)

    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup, disable_notification=True)
