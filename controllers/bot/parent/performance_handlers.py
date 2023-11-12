import logging

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from db.repositories.child_repository import ChildRepository
from services.api.alfa.cgi import CgiFetcher, CgiDataService
from services.api.alfa.customer import CustomerFetcher, CustomerDataService
from services.api.alfa.lesson import LessonFetcher
from services.bot.performance_service import PerformanceService
from utils.constants.callback_names import CPP
from utils.constants.messages import PPM_PERFORMANCE


def register_child_get_performance_handlers(bot):
    @bot.message_handler(func=lambda message: message.text.lower() == CPP.MENU_PERFORMANCE.lower())
    def performance_handler(message):
        message = bot.send_message(message.chat.id, CPP.MENU_PERFORMANCE)
        children = ChildRepository.find_children_by_parent_telegram_id(message.chat.id)
        if children is None:
            bot.edit_message_text(PPM_PERFORMANCE.ERROR_CHILDREN_NOT_FOUND,
                                  chat_id=message.chat.id, message_id=message.message_id)
            return

        children_amount = len(children)
        if children_amount == 1:
            child_selection(children[0].child_alfa_id, message)
        elif children_amount > 1:
            markup = InlineKeyboardMarkup(row_width=1)
            for child in children:
                button = InlineKeyboardButton(child.child_name, callback_data=f"{CPP.PERFORMANCE_S_C}_{child.child_alfa_id}")
                markup.add(button)
            bot.edit_message_text(PPM_PERFORMANCE.INFO_CHILD_SELECTION,
                                  chat_id=message.chat.id,
                                  message_id=message.message_id, reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith(f'{CPP.PERFORMANCE_S_C}_'))
    def child_selection_handler(call):
        child_alfa_id = int(call.data.split("_")[-1])
        child_selection(child_alfa_id, call.message)

    @bot.callback_query_handler(func=lambda call: call.data.startswith(f'{CPP.PERFORMANCE_S_G}_'))
    def group_selection_handler(call):
        data = call.data.split("_")
        child_alfa_id, child_group_alfa_id = int(data[-2]), int(data[-1])
        group_selection(child_alfa_id, child_group_alfa_id, call.message)

    @bot.callback_query_handler(func=lambda call: call.data.startswith(f'{CPP.PERFORMANCE_S_M}_'))
    def month_selection_handler(call):
        data = call.data.split("_")
        child_alfa_id, child_group_alfa_id, month = int(data[-3]), int(data[-2]), data[-1]
        month_selection(child_alfa_id, child_group_alfa_id, month, call.message)

    def child_selection(child_alfa_id, message):
        child_groups = CustomerDataService.get_customer_groups_by_customer_id(child_alfa_id)
        if child_groups is None:
            bot.edit_message_text(PPM_PERFORMANCE.ERROR_GROUPS_NOT_FOUND, chat_id=message.chat.id,
                                  message_id=message.message_id)
            return

        child_groups_amount = len(child_groups)
        if child_groups_amount == 1:
            group_selection(child_alfa_id, child_groups[0]["id"], message)
        elif child_groups_amount > 1:
            markup = InlineKeyboardMarkup(row_width=1)
            for group in child_groups:
                button = InlineKeyboardButton(group['name'],
                                              callback_data=f"{CPP.PERFORMANCE_S_G}_{child_alfa_id}_{group['id']}")
                markup.add(button)

            bot.edit_message_text(PPM_PERFORMANCE.INFO_GROUP_SELECTION,
                                  chat_id=message.chat.id, message_id=message.message_id, reply_markup=markup)

    def group_selection(child_alfa_id, group_alfa_id, message):
        month_names = CgiDataService.get_customer_studying_in_group_months(group_alfa_id, child_alfa_id)

        markup = InlineKeyboardMarkup(row_width=1)
        for month in month_names:
            date_y_m = month['year_month']
            button = InlineKeyboardButton(month["month_name"],
                                          callback_data=f"{CPP.PERFORMANCE_S_M}_{child_alfa_id}_{group_alfa_id}_{date_y_m}")
            markup.add(button)

        bot.edit_message_text(PPM_PERFORMANCE.INFO_MONTH_SELECTION,
                              chat_id=message.chat.id, message_id=message.message_id, reply_markup=markup)

    def month_selection(child_alfa_id, child_group_alfa_id, date_y_m, message):
        result = PerformanceService.get_performance(child_alfa_id, child_group_alfa_id, date_y_m)
        if result:
            topic_perf, teacher_fb, lessons_amount, attd_lessons_amount,average_att, average_grade = result
            msg = PPM_PERFORMANCE.RESULT(date_y_m,lessons_amount,average_grade,topic_perf,teacher_fb)
        else:
            msg = PPM_PERFORMANCE.ERROR_LESSONS_NOT_FOUND
        bot.edit_message_text(msg, chat_id=message.chat.id, message_id=message.message_id, reply_markup=None)


