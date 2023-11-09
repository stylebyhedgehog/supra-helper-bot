from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.repositories.parent_repository import ParentRepository
from services.api.alfa.customer import  CustomerService
from tests.utils import TestUtils
from utils.constants.messages import PPM_BALANCE_NOTIFICATION_DISPATCHING


def send_balance(lesson_info, bot):
    for child in lesson_info.get("details"):
        child_id = child.get("customer_id")
        res = CustomerService.get_child_balance_by_id(child_id)
        if res:
            name, balance, paid_count = res
            if int(paid_count) <= 1:
                parent = ParentRepository.find_parent_by_child_alfa_id(child_id)
                if parent:
                    markup = InlineKeyboardMarkup(row_width=1)
                    button_grp = InlineKeyboardButton(text="Пополнить баланс (Групповой формат)",
                                                      url="https://supraschool.ru/payment2023")
                    button_ind = InlineKeyboardButton(text="Пополнить баланс (Индивидуальный формат)",
                                                      url="https://supraschool.ru/indiv")
                    markup.add(button_grp, button_ind)
                    balance_info = PPM_BALANCE_NOTIFICATION_DISPATCHING.RESULT(balance, paid_count, name)
                    # bot.send_message(parent.telegram_id, balance_info, reply_markup=markup)
                    TestUtils.append_to_file("Отправлен: " + balance_info, "balance.txt")
