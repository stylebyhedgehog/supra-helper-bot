from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from db_func.repositories.child_repository import ChildRepository
from exceptions.bot_error_handler import bot_error_handler
from services.api.alfa.customer import CustomerDataService
from utils.logger import Logger

class SelectionChildGroupTemplate:
    def __init__(self, bot, menu_text, cpp_steps, ppm_messages, get_result_function, location):
        self.bot = bot
        self.menu_text = menu_text
        self.cpp_steps = cpp_steps
        self.ppm_messages = ppm_messages
        self.get_result_function = get_result_function
        self.location = location

        self.register_main_handler()
        self.register_child_selection_handler()
        self.register_group_selection_handler()

    def register_main_handler(self):
        @self.bot.message_handler(func=lambda message: message.text.lower() == self.menu_text.lower())
        @bot_error_handler(self.bot, self.location)
        def main_handler(message):
            message = self.bot.send_message(message.chat.id, self.menu_text)
            children = ChildRepository.find_by_parent_telegram_id(message.chat.id)
            if children is None:
                self.bot.edit_message_text(self.ppm_messages.ERROR_CHILDREN_NOT_FOUND,
                                           chat_id=message.chat.id, message_id=message.message_id)
                Logger.bot_handled_error(message.chat.id, self.location, f"Parent's children not found")
                return

            children_amount = len(children)
            if children_amount == 1:
                self.child_selection(children[0].child_alfa_id, message)
            elif children_amount > 1:
                markup = InlineKeyboardMarkup(row_width=1)
                for child in children:
                    button = InlineKeyboardButton(child.child_name,
                                                  callback_data=f"{self.cpp_steps.S_C}_{child.child_alfa_id}")
                    markup.add(button)
                self.bot.edit_message_text(self.ppm_messages.INFO_CHILD_SELECTION,
                                           chat_id=message.chat.id,
                                           message_id=message.message_id, reply_markup=markup)

    def register_child_selection_handler(self):
        @self.bot.callback_query_handler(func=lambda call: call.data.startswith(f'{self.cpp_steps.S_C}_'))
        @bot_error_handler(self.bot, self.location)
        def child_selection_handler(call):
            child_alfa_id = int(call.data.split("_")[-1])
            self.child_selection(child_alfa_id, call.message)

    def register_group_selection_handler(self):
        @self.bot.callback_query_handler(func=lambda call: call.data.startswith(f'{self.cpp_steps.S_G}_'))
        @bot_error_handler(self.bot, self.location)
        def group_selection_handler(call):
            data = call.data.split("_")
            child_alfa_id, child_group_alfa_id = int(data[-2]), int(data[-1])
            self.group_selection(child_alfa_id, child_group_alfa_id, call.message)


    def child_selection(self, child_alfa_id, message):
        child_groups = CustomerDataService.get_customer_groups_by_customer_id(child_alfa_id)
        if child_groups is None:
            self.handle_groups_not_found(child_alfa_id, message)
            return

        child_groups_amount = len(child_groups)
        if child_groups_amount == 1:
            self.group_selection(child_alfa_id, child_groups[0]["id"], message)
        elif child_groups_amount > 1:
            markup = InlineKeyboardMarkup(row_width=1)
            for group in child_groups:
                button = InlineKeyboardButton(group['name'],
                                              callback_data=f"{self.cpp_steps.S_G}_{child_alfa_id}_{group['id']}")
                markup.add(button)

            self.bot.edit_message_text(self.ppm_messages.INFO_GROUP_SELECTION,
                                       chat_id=message.chat.id, message_id=message.message_id, reply_markup=markup)

    def handle_groups_not_found(self, child_alfa_id, message):
        self.bot.edit_message_text(self.ppm_messages.ERROR_GROUPS_NOT_FOUND, chat_id=message.chat.id,
                                   message_id=message.message_id)
        Logger.bot_handled_error(message.chat.id, self.location,
                                 f"Groups for child with alfa_id={child_alfa_id} not found")

    def group_selection(self, child_alfa_id, group_alfa_id, message):
        pass


