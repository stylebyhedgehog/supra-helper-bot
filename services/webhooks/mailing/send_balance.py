import os

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from db_func.repositories.parent_repository import ParentRepository
from services.api.alfa.customer import CustomerDataService
from services.api.alfa.group import GroupDataService
from utils.constants.messages import PPM_BALANCE_EXPIRATION_NOTIFICATION_DISPATCHING
from utils.file_utils import FileUtil
from utils.logger import Logger


class BalanceMailer:
    @staticmethod
    def send_balance_on_expiration(bot, lesson_info):
        for child in lesson_info.get("details"):
            if child.get("is_attend") == 0 and child.get("reason_id") == 7:
                continue
            child_id = child.get("customer_id")
            res = CustomerDataService.get_child_balance_by_id(child_id)
            if res:
                name, balance, paid_count = res
                if int(paid_count) <= 1:
                    group_id = lesson_info.get("group_ids")[0]
                    date = lesson_info.get("date")

                    parent = ParentRepository.find_by_child_alfa_id(child_id)
                    if paid_count == 1:
                        balance_info = PPM_BALANCE_EXPIRATION_NOTIFICATION_DISPATCHING.RESULT_ONE_REMAINS(balance, paid_count, name)
                    else:
                        balance_info = PPM_BALANCE_EXPIRATION_NOTIFICATION_DISPATCHING.RESULT_ZERO_REMAINS(balance, paid_count, name)
                    BalanceMailer._write_in_json(child_id, group_id, date, balance_info, parent)
                    BalanceMailer._send_notification_message(parent, balance_info, bot)
            else:
                Logger.mailing_handled_error("mailing_balance", f"Error on receiving balance of child with alfa_id={child_id}")

    @staticmethod
    def send_balance_on_payment(bot, lesson_info):
        pass

    @staticmethod
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
            Logger.mailing_handled_error("mailing_balance", f"Error on writing in file: {e}")

    @staticmethod
    def _send_notification_message(parent, info, bot):
        if os.getenv("MAILING_MODE") == "1":
            if parent:
                markup = InlineKeyboardMarkup(row_width=1)
                button_grp = InlineKeyboardButton(text="Пополнить баланс (Групповой формат)",
                                                  url="https://supraschool.ru/payment2023")
                button_ind = InlineKeyboardButton(text="Пополнить баланс (Индивидуальный формат)",
                                                  url="https://supraschool.ru/indiv")
                markup.add(button_grp, button_ind)
                bot.send_message(parent.telegram_id, info, reply_markup=markup)
                Logger.mailing_info(parent.telegram_id, "mailing_balance", "Successfully mailed")

