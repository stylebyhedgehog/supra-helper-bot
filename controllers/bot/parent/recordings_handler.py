from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from controllers.bot.parent.selection_child_group_template import SelectionChildGroupTemplate
from exceptions.bot_error_handler import bot_error_handler
from services.api.alfa.cgi import CgiDataService
from services.api.alfa.lesson import LessonDataService
from services.api.alfa.subject import SubjectDataService
from services.bot.recordings_service import RecordingsService
from utils.logger import Logger
from utils.string_utils import StringUtil
from services.bot.performance_service import PerformanceService
from utils.constants.callback_names import CPP_PERFORMANCE, CPP_MENU, CPP_RECORDINGS
from utils.constants.messages import PPM_PERFORMANCE, PPM_RECORDINGS


class RecordingsHandler(SelectionChildGroupTemplate):
    def __init__(self, bot):
        super().__init__(bot, CPP_MENU.RECORDINGS, CPP_RECORDINGS, PPM_RECORDINGS, RecordingsService.get_recording_by_lesson_id, "recordings")
        self.register_lesson_selection_handler()

    def register_lesson_selection_handler(self):
        @self.bot.callback_query_handler(func=lambda call: call.data.startswith(f'{self.cpp_steps.S_L}_'))
        @bot_error_handler(self.bot, self.location)
        def lesson_selection_handler(call):
            data = call.data.split("_")
            child_alfa_id, child_group_alfa_id, lesson_id = int(data[-3]), int(data[-2]), data[-1]
            self.lesson_selection(child_alfa_id, child_group_alfa_id, lesson_id, call.message)

    def group_selection(self, child_alfa_id, group_alfa_id, message):
        lessons = LessonDataService.get_child_lessons_info_for_week(child_alfa_id, group_alfa_id)
        if lessons:
            markup = InlineKeyboardMarkup(row_width=1)
            for lesson in lessons:
                btn_name = f"({lesson['date']}) {lesson['topic']}"
                lesson_id = lesson['id']
                button = InlineKeyboardButton(btn_name,
                                              callback_data=f"{self.cpp_steps.S_L}_{child_alfa_id}_{group_alfa_id}_{lesson_id}")
                markup.add(button)

            self.bot.edit_message_text(self.ppm_messages.INFO_LESSON_SELECTION,
                                       chat_id=message.chat.id, message_id=message.message_id, reply_markup=markup)
        else:
            self.bot.edit_message_text(self.ppm_messages.ERROR_LESSONS_NOT_FOUND, chat_id=message.chat.id,
                                       message_id=message.message_id)
            Logger.bot_handled_error(message.chat.id, self.location,
                                     f"Lessons for child with alfa_id={child_alfa_id} in group with alfa_id={group_alfa_id} not found")

    def lesson_selection(self, child_alfa_id, child_group_alfa_id, lesson_id, message):
        res = self.get_result_function(lesson_id)
        if res:
            msg = self.ppm_messages.RESULT(*res)
            self.bot.edit_message_text(msg, chat_id=message.chat.id, message_id=message.message_id, reply_markup=None)
            Logger.bot_info(message.chat.id, self.location,
                            f"recording for child with alfa_id={child_alfa_id} in group with alfa_id={child_group_alfa_id} for lesson with alda_id={lesson_id} successfully formed")
        else:
            msg = self.ppm_messages.ERROR_RECORDING_NOT_FOUND
            self.bot.edit_message_text(msg, chat_id=message.chat.id, message_id=message.message_id, reply_markup=None)
            Logger.bot_handled_error(message.chat.id, self.location,
                                     f"recording info for child with alfa_id={child_alfa_id} in group with alfa_id={child_group_alfa_id} for lesson with alda_id={lesson_id} not formed")

