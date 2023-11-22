from dotenv import load_dotenv
import telebot
from flask import Flask
import os

from controllers.bot.admin.auth_handler import register_admin_auth_handlers
from controllers.bot.admin.authed_parents_handlers import register_authed_parents_handlers
from controllers.bot.menu_handlers import register_menu_handlers
from controllers.bot.parent.attendance_handlers import register_attendance_handlers
from controllers.bot.parent.auth_handlers import register_parent_auth_handlers
from controllers.bot.parent.balance_handlers import register_balance_handlers
from controllers.bot.parent.contact_administrator_handler import register_contact_administrator_handlers
from controllers.bot.parent.performance_handlers import register_performance_handlers
from controllers.flask.admin_panel_controllers import register_admin_panel_controllers
from controllers.flask.log_controller import register_log_controllers
from controllers.flask.mailing_result_controllers import register_mailing_results_controllers
from controllers.flask.external_webhook_controllers import register_external_webhook_controllers
from controllers.flask.test_controllers import register_test_controllers

from data_storages.db.core import DatabaseManager
from services.admin_service import clear_all_tables
from services.api.alfa.cgi import CgiDataService
from services.mailing.mailer import Mailer
from utils.file_utils import FileUtil


load_dotenv()
DatabaseManager.init_db('sqlite:///' + FileUtil.get_path_to_db())
app = Flask(__name__)
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"), threaded=False)

register_menu_handlers(bot)
register_admin_auth_handlers(bot)
register_parent_auth_handlers(bot)
register_contact_administrator_handlers(bot)
register_authed_parents_handlers(bot)
register_performance_handlers(bot)
register_attendance_handlers(bot)
register_balance_handlers(bot)

mailer = Mailer(bot)

#todo изменить процесс авторизации родителей
#todo разворачивать бд автоматически, создавать json и txt файлы автоматически
#todo выяснить в чем проблема при send_recordings_on_recording_completed в многопоточной среде
#todo добавить вебхуки в альфа и зум

if os.getenv("DEV_MODE") == "0":

    register_admin_panel_controllers(app)
    register_external_webhook_controllers(app, bot, mailer)
    register_mailing_results_controllers(app)
    register_test_controllers(app, mailer)
    register_log_controllers(app)


else:
    # import tracemalloc
    # print("start")
    #
    # file_path1 = FileUtil.get_path_to_mailing_results_file("recordings.json")
    # file_path2 = FileUtil.get_path_to_mailing_results_file("reports.json")
    # file_path3 = FileUtil.get_path_to_mailing_results_file("balance.json")
    # FileUtil.clear_json(file_path1)
    # FileUtil.clear_json(file_path2)
    # FileUtil.clear_json(file_path3)
    # clear_all_tables()
    #
    # tracemalloc.start()
    #
    # test_manager = TestManager(mailer)
    # # test_manager.execute_auth_all_parents_test(TestMode.MULTY_THREAD)
    # test_manager.execute_mailing_tests(TestMode.ONE_THREAD)
    #
    #
    # current, peak = tracemalloc.get_traced_memory()
    # tracemalloc.stop()
    # print(f"Current memory usage is {current / 10 ** 6}MB; Peak was {peak / 10 ** 6}MB")
    # print("end")
    # register_admin_panel_controllers(app)
    # register_external_webhook_controllers(app, bot, mailer)
    # register_mailing_results_controllers(app)
    # register_test_controllers(app, mailer)
    # register_log_controllers(app)
    # app.run()
    # bot.stop_bot()
    # bot.remove_webhook()
    # clear_all_tables()
    bot.polling(none_stop=True)

