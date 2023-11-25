from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from controllers.bot.parent.selection_child_group_template import SelectionChildGroupTemplate
from exceptions.bot_error_handler import bot_error_handler
from services.api.alfa.cgi import CgiDataService
from services.api.alfa.lesson import LessonDataService
from services.api.alfa.subject import SubjectDataService
from utils.logger import Logger
from utils.string_utils import StringUtil


class StudyResultsHandler(SelectionChildGroupTemplate):
    def __init__(self, bot, menu_text, cpp_steps, ppm_messages, get_result_function, location):
        super().__init__(bot, menu_text, cpp_steps, ppm_messages, get_result_function, location)
        self.register_month_selection_handler()

    def register_month_selection_handler(self):
        @self.bot.callback_query_handler(func=lambda call: call.data.startswith(f'{self.cpp_steps.S_M}_'))
        @bot_error_handler(self.bot, self.location)
        def month_selection_handler(call):
            data = call.data.split("_")
            child_alfa_id, child_group_alfa_id, month = int(data[-3]), int(data[-2]), data[-1]
            self.month_selection(child_alfa_id, child_group_alfa_id, month, call.message)

    def group_selection(self, child_alfa_id, group_alfa_id, message):
        if not self._is_available(group_alfa_id):
            self.bot.edit_message_text(self.ppm_messages.INFO_NOT_AVAILABLE,
                                       chat_id=message.chat.id, message_id=message.message_id)
            return
        month_names = CgiDataService.get_customer_studying_in_group_months(group_alfa_id, child_alfa_id)
        markup = InlineKeyboardMarkup(row_width=1)
        if month_names:
            for month in month_names:
                date_y_m = month['year_month']
                button = InlineKeyboardButton(month["month_name"],
                                              callback_data=f"{self.cpp_steps.S_M}_{child_alfa_id}_{group_alfa_id}_{date_y_m}")
                markup.add(button)

            self.bot.edit_message_text(self.ppm_messages.INFO_MONTH_SELECTION,
                                       chat_id=message.chat.id, message_id=message.message_id, reply_markup=markup)
        else:
            self.bot.edit_message_text(self.ppm_messages.ERROR_MONTHS_NOT_FOUND, chat_id=message.chat.id,
                                       message_id=message.message_id)
            Logger.bot_handled_error(message.chat.id, self.location,
                                     f"Months of education for child with alfa_id={child_alfa_id} in group with alfa_id={group_alfa_id} not found")

    def month_selection(self, child_alfa_id, child_group_alfa_id, date_y_m, message):
        data = self.get_result_function(child_alfa_id, child_group_alfa_id, date_y_m)
        if data:
            msg = self.ppm_messages.RESULT(*data)
            self.bot.edit_message_text(msg, chat_id=message.chat.id, message_id=message.message_id, reply_markup=None)
            Logger.bot_info(message.chat.id, self.location,
                            f"{self.location} info for child with alfa_id={child_alfa_id} in group with alfa_id={child_group_alfa_id} by period {date_y_m} successfully formed")
        else:
            msg = self.ppm_messages.ERROR_LESSONS_NOT_FOUND
            self.bot.edit_message_text(msg, chat_id=message.chat.id, message_id=message.message_id, reply_markup=None)
            Logger.bot_handled_error(message.chat.id, self.location,
                                     f"{self.location} info for child with alfa_id={child_alfa_id} in group with alfa_id={child_group_alfa_id} by period {date_y_m} not formed")

    def _is_available(self, group_alfa_id):  # check availability to watch performance based on course name
        if self.location == "performance":
            subject_id = LessonDataService.get_subject_id_by_group_id(group_alfa_id)
            if subject_id:
                full_subject_name = SubjectDataService.get_subject_name(subject_id)
                course_name, subject_name = StringUtil.extract_course_subject(full_subject_name)
                if StringUtil.is_english_course(course_name):
                    return False

        return True
