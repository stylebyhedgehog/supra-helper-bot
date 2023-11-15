import os

from telebot import types

from exceptions.bot_error_handler import bot_error_handler
from services.bot.authentication_service import AuthenticationService
from utils.constants.callback_names import CPP, CAP
from utils.constants.messages import MENU


def register_menu_handlers(bot):
    @bot.message_handler(commands=['start', 'help'])
    @bot_error_handler(bot)
    def handle_help(message):
        #todo вынести в команду /help_admin

        # if AuthenticationService.is_admin_authorized(message.chat.id):
        #     admin_menu(bot, message)
        # else:
        #     bot.send_message(message.chat.id, MENU.INFO_INIT)

        if AuthenticationService.is_parent_authorized(message.chat.id):
            bot.send_message(message.chat.id, MENU.INFO_AUTHED, reply_markup=parent_menu())
        else:
            bot.send_message(message.chat.id, MENU.INFO_INIT)


def parent_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for row in CPP.menu:
        markup.add(*[types.KeyboardButton(button) for button in row])
    return markup


def admin_menu(bot, message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for button_info in CAP.menu:
        button = types.InlineKeyboardButton(button_info['text'], callback_data=button_info['callback_data'])
        markup.add(button)

    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup, disable_notification=True)
