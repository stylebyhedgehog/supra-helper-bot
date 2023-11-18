import logging

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from data_storages.db.repositories.parent_repository import ParentRepository
from services.api.alfa.customer import CustomerDataService
from services.api.alfa.group import GroupDataService
from utils.constants.messages import PPM_BALANCE_NOTIFICATION_DISPATCHING
from utils.file_utils import FileUtil


def send_balance(lesson_info, bot):
    for child in lesson_info.get("details"):
        child_id = child.get("customer_id")
        res = CustomerDataService.get_child_balance_by_id(child_id)
        if res:
            name, balance, paid_count = res
            if int(paid_count) <= 1:
                parent = ParentRepository.find_by_child_alfa_id(child_id)
                balance_info = PPM_BALANCE_NOTIFICATION_DISPATCHING.RESULT(balance, paid_count, name)
                # _send_notification_message(parent, balance_info, bot)
                _write_in_json(child_id, lesson_info.get("group_ids")[0], lesson_info.get("date"),balance_info, parent)


def _write_in_json(child_id, group_id, date, info, parent):
    try:
        path = FileUtil.get_path_to_mailing_results_file("balance.json")

        status = "Не отправлен (Родитель не зарегистрирован в системе)"
        if parent:
            status = "Отправлен"
        data = {
            "group_name": GroupDataService.get_group_name_by_id(group_id),
            "child_name": CustomerDataService.get_child_name_by_id(child_id),
            "date": date,
            "report": info,
            "status": status
        }
        FileUtil.add_to_json_file(data, path)
    except Exception as e:
        logging.error(f"Ошибка записи информации о балансе в файл {e}")


def _send_notification_message(parent, info, bot):
    if parent:
        markup = InlineKeyboardMarkup(row_width=1)
        button_grp = InlineKeyboardButton(text="Пополнить баланс (Групповой формат)",
                                          url="https://supraschool.ru/payment2023")
        button_ind = InlineKeyboardButton(text="Пополнить баланс (Индивидуальный формат)",
                                          url="https://supraschool.ru/indiv")
        markup.add(button_grp, button_ind)
        bot.send_message(parent.telegram_id, info, reply_markup=markup)
