from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from db_func.repositories.child_repository import ChildRepository
from exceptions.bot_error_handler import bot_error_handler
from services.api.alfa.cgi import CgiDataService
from services.api.alfa.customer import CustomerDataService
from services.api.alfa.lesson import LessonDataService
from services.api.alfa.subject import SubjectDataService
from utils.constants.messages import PPM_STUDY_RESULTS
from utils.logger import Logger
from utils.string_utils import StringUtil


def register_study_results_handlers(bot, menu_text, cpp_steps, ppm_messages: PPM_STUDY_RESULTS, get_result_function,
                                    location):
    @bot.message_handler(func=lambda message: message.text.lower() == menu_text.lower())
    @bot_error_handler(bot, location)
    def main_handler(message):
        message = bot.send_message(message.chat.id, menu_text)
        children = ChildRepository.find_by_parent_telegram_id(message.chat.id)
        if children is None:
            bot.edit_message_text(ppm_messages.ERROR_CHILDREN_NOT_FOUND,
                                  chat_id=message.chat.id, message_id=message.message_id)
            Logger.bot_handled_error(message.chat.id, location, f"Parent's children not found")
            return

        children_amount = len(children)
        if children_amount == 1:
            child_selection(children[0].child_alfa_id, message)
        elif children_amount > 1:
            markup = InlineKeyboardMarkup(row_width=1)
            for child in children:
                button = InlineKeyboardButton(child.child_name,
                                              callback_data=f"{cpp_steps.S_C}_{child.child_alfa_id}")
                markup.add(button)
            bot.edit_message_text(ppm_messages.INFO_CHILD_SELECTION,
                                  chat_id=message.chat.id,
                                  message_id=message.message_id, reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith(f'{cpp_steps.S_C}_'))
    @bot_error_handler(bot, location)
    def child_selection_handler(call):
        child_alfa_id = int(call.data.split("_")[-1])
        child_selection(child_alfa_id, call.message)

    @bot.callback_query_handler(func=lambda call: call.data.startswith(f'{cpp_steps.S_G}_'))
    @bot_error_handler(bot, location)
    def group_selection_handler(call):
        data = call.data.split("_")
        child_alfa_id, child_group_alfa_id = int(data[-2]), int(data[-1])
        group_selection(child_alfa_id, child_group_alfa_id, call.message)

    @bot.callback_query_handler(func=lambda call: call.data.startswith(f'{cpp_steps.S_M}_'))
    @bot_error_handler(bot, location)
    def month_selection_handler(call):
        data = call.data.split("_")
        child_alfa_id, child_group_alfa_id, month = int(data[-3]), int(data[-2]), data[-1]
        month_selection(child_alfa_id, child_group_alfa_id, month, call.message)

    @bot_error_handler(bot, location)
    def child_selection(child_alfa_id, message):
        child_groups = CustomerDataService.get_customer_groups_by_customer_id(child_alfa_id)
        if child_groups is None:
            bot.edit_message_text(ppm_messages.ERROR_GROUPS_NOT_FOUND, chat_id=message.chat.id,
                                  message_id=message.message_id)
            Logger.bot_handled_error(message.chat.id, location,
                                     f"Groups for child with alfa_id={child_alfa_id} not found")
            return

        child_groups_amount = len(child_groups)
        if child_groups_amount == 1:
            group_selection(child_alfa_id, child_groups[0]["id"], message)
        elif child_groups_amount > 1:
            markup = InlineKeyboardMarkup(row_width=1)
            for group in child_groups:
                button = InlineKeyboardButton(group['name'],
                                              callback_data=f"{cpp_steps.S_G}_{child_alfa_id}_{group['id']}")
                markup.add(button)

            bot.edit_message_text(ppm_messages.INFO_GROUP_SELECTION,
                                  chat_id=message.chat.id, message_id=message.message_id, reply_markup=markup)

    @bot_error_handler(bot, location)
    def group_selection(child_alfa_id, group_alfa_id, message):
        if not _is_available(group_alfa_id, location):
            bot.edit_message_text(ppm_messages.INFO_NOT_AVAILABLE,
                                  chat_id=message.chat.id, message_id=message.message_id)
            return
        month_names = CgiDataService.get_customer_studying_in_group_months(group_alfa_id, child_alfa_id)
        markup = InlineKeyboardMarkup(row_width=1)
        if month_names:
            for month in month_names:
                date_y_m = month['year_month']
                button = InlineKeyboardButton(month["month_name"],
                                              callback_data=f"{cpp_steps.S_M}_{child_alfa_id}_{group_alfa_id}_{date_y_m}")
                markup.add(button)

            bot.edit_message_text(ppm_messages.INFO_MONTH_SELECTION,
                                  chat_id=message.chat.id, message_id=message.message_id, reply_markup=markup)
        else:
            bot.edit_message_text(ppm_messages.ERROR_MONTHS_NOT_FOUND, chat_id=message.chat.id,
                                  message_id=message.message_id)
            Logger.bot_handled_error(message.chat.id, location,
                                     f"Months of education for child with alfa_id={child_alfa_id} in group with alfa_id={group_alfa_id} not found")

    @bot_error_handler(bot, location)
    def month_selection(child_alfa_id, child_group_alfa_id, date_y_m, message):
        data = get_result_function(child_alfa_id, child_group_alfa_id, date_y_m)
        if data:
            msg = ppm_messages.RESULT(*data)
            bot.edit_message_text(msg, chat_id=message.chat.id, message_id=message.message_id, reply_markup=None)
            Logger.bot_info(message.chat.id, location,
                            f"{location} info for child with alfa_id={child_alfa_id} in group with alfa_id={child_group_alfa_id} by period {date_y_m} successfully formed")


        else:
            msg = ppm_messages.ERROR_LESSONS_NOT_FOUND
            bot.edit_message_text(msg, chat_id=message.chat.id, message_id=message.message_id, reply_markup=None)
            Logger.bot_handled_error(message.chat.id, location,
                                     f"{location} info for child with alfa_id={child_alfa_id} in group with alfa_id={child_group_alfa_id} by period {date_y_m} not formed")

    def _is_available(group_alfa_id, loc):  # check availability to watch performance based on course name
        if loc == "performance":
            subject_id = LessonDataService.get_subject_id_by_group_id(group_alfa_id)
            if subject_id:
                full_subject_name = SubjectDataService.get_subject_name(subject_id)
                course_name, subject_name = StringUtil.extract_course_subject(full_subject_name)
                if StringUtil.is_english_course(course_name):
                    return False

        return True
