import logging

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from db.repositories.child_repository import ChildRepository
from services.api.alfa.customer import FetchCustomer, CustomerService
from utils.constants.callback_names import CPP
from utils.constants.messages import PPM_BALANCE


def register_child_get_balance(bot):
    @bot.message_handler(func=lambda message: message.text.lower() == CPP.MENU_BALANCE.lower())
    def get_balance_handler(message):
        message = bot.send_message(message.chat.id, CPP.MENU_BALANCE)
        children = ChildRepository.find_children_by_parent_telegram_id(message.chat.id)
        if children is None:
            bot.edit_message_text(message.chat.id, PPM_BALANCE.ERROR_CHILDREN_NOT_FOUND)

        children_amount = len(children)
        if children_amount == 1:
            get_balance_child_selection(children[0].child_alfa_id, message)
        elif children_amount > 1:
            markup = InlineKeyboardMarkup(row_width=1)
            for child in children:
                button = InlineKeyboardButton(child.child_name, callback_data=f"{CPP.BALANCE_S_C}_{child.child_alfa_id}")
                markup.add(button)
            bot.edit_message_text(PPM_BALANCE.INFO_CHILD_SELECTION,
                                  chat_id=message.chat.id, message_id=message.message_id, reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith(f'{CPP.BALANCE_S_C}_'))
    def get_balance_child_selection_handler(call):
        child_alfa_id = int(call.data.split("_")[-1])
        get_balance_child_selection(child_alfa_id, call.message)

    def get_balance_child_selection(child_alfa_id, message):
        result = CustomerService.get_child_balance_by_id(child_alfa_id)
        markup = None
        if result:
            name, balance, paid_count = result
            if paid_count <= 1:
                markup = InlineKeyboardMarkup(row_width=1)
                button_grp = InlineKeyboardButton(text="Пополнить баланс (Групповой формат)", url="https://supraschool.ru/payment2023")
                button_ind = InlineKeyboardButton(text="Пополнить баланс (Индивидуальный формат)", url="https://supraschool.ru/indiv")
                markup.add(button_grp, button_ind)
            msg = PPM_BALANCE.RESULT(name, balance, paid_count)
        else:
            msg = PPM_BALANCE.ERROR_UNHANDLED
        bot.edit_message_text(msg, chat_id=message.chat.id, message_id=message.message_id, reply_markup=markup)
