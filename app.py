from dotenv import load_dotenv
import telebot
from flask import Flask
import os

from controllers.bot.admin.auth_handler import register_admin_auth_handlers
from controllers.bot.admin.authed_parents_handlers import register_authed_parents_handlers
from controllers.bot.menu_handlers import register_menu_handlers
from controllers.bot.parent.attendance_handlers import  AttendanceHandler
from controllers.bot.parent.auth_handlers import register_parent_auth_handlers
from controllers.bot.parent.balance_handlers import register_balance_handlers
from controllers.bot.parent.contact_administrator_handler import register_contact_administrator_handlers
from controllers.bot.parent.performance_handlers import  PerformanceHandler
from controllers.bot.parent.recordings_handler import RecordingsHandler
from controllers.flask.admin_panel_controllers import register_admin_panel_controllers
from controllers.flask.log_controller import register_log_controllers
from controllers.flask.mailing_result_controllers import register_mailing_results_controllers
from controllers.flask.external_webhook_controllers import register_external_webhook_controllers
from controllers.flask.test_controllers import register_test_controllers

from db_func.core import DatabaseManager
from services.admin_service import clear_all_tables, clear_mailing_results, clear_logs
from services.mailing.mailer import Mailer
from services.mailing.send_recordings_on_recording_completed import RecordingMailerOnRecordingCompleted
from utils.file_utils import FileUtil


load_dotenv()
# Initialize db. If where are no db file it will be created with all tables from models
DatabaseManager.init_db('sqlite:///' + FileUtil.get_path_to_db())
app = Flask(__name__)

if os.getenv("DEV_MODE") == "1":
    bot = telebot.TeleBot(os.getenv("DEV_BOT_TOKEN"), threaded=False)
else:
    bot = telebot.TeleBot(os.getenv("BOT_TOKEN"), threaded=False)
# Create log files and mailing_results files if not exists
FileUtil.create_log_and_mailing_results_files()

register_menu_handlers(bot)
register_admin_auth_handlers(bot)
register_parent_auth_handlers(bot)
register_contact_administrator_handlers(bot)
register_authed_parents_handlers(bot)
per = PerformanceHandler(bot)
att = AttendanceHandler(bot)
rec = RecordingsHandler(bot)
register_balance_handlers(bot)

mailer = Mailer(bot)

#todo изменить процесс авторизации родителей
#todo добавить вебхуки в альфа для изменения перечня детей у родителя
#todo реализовать автоочистку lesson_with_absent_children и absent_children
#todo реализовать автоочистку логов и разосланной информации
#todo zoom api добавить пагинацию
#todo доделать уведомление при пополнении баланса

# todo в некоторых вебхуках лишние / (у альфы) и у зума тоже убрать

# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     # Отправка сообщения
#     sent_message = bot.send_message(message.chat.id, "Привет, это ваше сообщение!")
#
#     # Получение идентификатора чата и сообщения
#     chat_id = sent_message.chat.id
#     message_id = sent_message.message_id
#
#     # Теперь можно проверить, было ли сообщение отправлено пользователю
#     if message.chat.id == chat_id and message.message_id == message_id:
#         print("Сообщение было успешно отправлено пользователю!")




if os.getenv("DEV_MODE") == "0":

    register_external_webhook_controllers(app, bot, mailer)
    register_mailing_results_controllers(app)
    register_test_controllers(app, mailer)
    register_log_controllers(app)
    register_admin_panel_controllers(app)

    if __name__ == '__main__':
        app.run(port=5000)

else:
    # # test_manager.execute_auth_all_parents_test(TestMode.MULTY_THREAD)
    #

    # test_manager = TestManager(mailer)
    # test_manager.execute_mailing_tests(TestMode.MULTY_THREAD)

    # bot.stop_bot()
    # bot.remove_webhook()
    # clear_all_tables()
    # clear_mailing_results()
    # clear_logs()
    # register_admin_panel_controllers(app)
    # register_external_webhook_controllers(app, bot, mailer)
    # register_mailing_results_controllers(app)
    # register_test_controllers(app, mailer)
    # register_log_controllers(app)
    # app.run()



    # register_admin_panel_controllers(app)
    # register_external_webhook_controllers(app, bot, mailer)
    # register_mailing_results_controllers(app)
    # register_test_controllers(app, mailer)
    # register_log_controllers(app)
    # if __name__ == '__main__':
    #     app.run(port=5000)
    #
    x = RecordingMailerOnRecordingCompleted.get_lesson_id_by_group_id_date_zoom_topic(145, "2023-12-04", "Веб-программирование frontend_2 пн/ср 19:30 [145]")
    print(x)
    pass
    # bot.polling(none_stop=True)

