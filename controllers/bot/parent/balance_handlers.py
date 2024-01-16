from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from db_func.repositories.child_repository import ChildRepository
from db_func.repositories.payment_link_repository import PaymentLinkRepository
from exceptions.bot_error_handler import bot_error_handler
from services.api.alfa.customer import CustomerDataService
from utils.constants.callback_names import CPP_MENU, CPP_BALANCE
from utils.constants.messages import PPM_BALANCE
from utils.date_utils import DateUtil
from utils.logger import Logger


def register_balance_handlers(bot):
    @bot.message_handler(func=lambda message: message.text.lower() == CPP_MENU.BALANCE.lower())
    @bot_error_handler(bot)
    def get_balance_handler(message):
        message = bot.send_message(message.chat.id, CPP_MENU.BALANCE)
        children = ChildRepository.find_by_parent_telegram_id(message.chat.id)
        if children is None:
            bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                  text=PPM_BALANCE.ERROR_CHILDREN_NOT_FOUND)
            Logger.bot_handled_error(message.chat.id, "balance", f"Parent's children not found")
            return

        children_amount = len(children)
        if children_amount == 1:
            get_balance_child_selection(children[0].child_alfa_id, message)
        elif children_amount > 1:
            markup = InlineKeyboardMarkup(row_width=1)
            for child in children:
                button = InlineKeyboardButton(child.child_name,
                                              callback_data=f"{CPP_BALANCE.S_C}_{child.child_alfa_id}")
                markup.add(button)
            bot.edit_message_text(PPM_BALANCE.INFO_CHILD_SELECTION,
                                  chat_id=message.chat.id, message_id=message.message_id, reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith(f'{CPP_BALANCE.S_C}_'))
    @bot_error_handler(bot)
    def get_balance_child_selection_handler(call):
        child_alfa_id = int(call.data.split("_")[-1])
        get_balance_child_selection(child_alfa_id, call.message)

    @bot_error_handler(bot)
    def get_balance_child_selection(child_alfa_id, message):
        result = CustomerDataService.get_child_balance_by_id(child_alfa_id)
        markup = None
        if result:
            name, balance, paid_count = result
            if paid_count <= 1:
                markup = InlineKeyboardMarkup(row_width=1)
                button_grp = InlineKeyboardButton(text="Пополнить баланс (Групповой формат)",
                                                  url=PaymentLinkRepository.get_group_payment_link())
                button_ind = InlineKeyboardButton(text="Пополнить баланс (Индивидуальный формат)",
                                                  url=PaymentLinkRepository.get_individual_payment_link())
                markup.add(button_grp, button_ind)

            current_date_y_m_d = DateUtil.get_current_moscow_date_y_m_d_as_str()
            msg = PPM_BALANCE.RESULT(name, balance, paid_count, current_date_y_m_d)
            bot.edit_message_text(msg, chat_id=message.chat.id, message_id=message.message_id, reply_markup=markup)
            Logger.bot_info(message.chat.id, "balance",
                            f"Balance info for child with alfa_id={child_alfa_id} successfully formed")
        else:
            msg = PPM_BALANCE.ERROR_UNHANDLED
            bot.edit_message_text(msg, chat_id=message.chat.id, message_id=message.message_id, reply_markup=markup)
            Logger.bot_handled_error(message.chat.id,"balance", f"Balance info for child with alfa_id={child_alfa_id} not formed")
