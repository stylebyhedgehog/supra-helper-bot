from dotenv import load_dotenv
import telebot
from flask import Flask, request, jsonify
import os

from controllers.bot.admin.authed_parents_handlers import register_authed_parents_handlers
from controllers.bot.menu_handlers import register_menu_handlers
from controllers.bot.parent.attendance_handlers import register_attendance_handlers
from controllers.bot.parent.auth_handlers import register_parent_auth_handlers
from controllers.bot.parent.balance_handlers import register_balance_handlers
from controllers.bot.parent.contact_administrator_handler import register_contact_administrator_handlers
from controllers.bot.parent.performance_handlers import register_performance_handlers

from data_storages.db.core import DatabaseManager
from services.admin_service import clear_all_tables
from services.api.alfa.lesson import LessonFetcher
from services.mailing.mailer import Mailer
from tests.tests_manager import TestManager, TestMode

from utils.encryption import Encryption
from utils.file_utils import FileUtil


load_dotenv()
DatabaseManager.init_db('sqlite:///' + FileUtil.get_path_to_db())
app = Flask(__name__)
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"), threaded=False)


register_menu_handlers(bot)
register_parent_auth_handlers(bot)
register_contact_administrator_handlers(bot)
register_authed_parents_handlers(bot)
register_performance_handlers(bot)
register_attendance_handlers(bot)
register_balance_handlers(bot)


mailer = Mailer(bot)


if os.getenv("DEV_MODE") == "0":
    @app.route('/' + os.getenv("BOT_TOKEN"), methods=['POST'])
    def getMessage():
        json_str = request.get_data().decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return '', 200


    @app.route('/zoom_webhook/recordings/', methods=['POST'])  # todo добавить вебхук в zoom
    def zoom_webhook():
        if request.method == "POST":
            if request.json["event"] == "endpoint.url_validation":
                res = Encryption.generate_encrypted_token(request.json, os.getenv("ZOOM_SECRET"))
                return jsonify(res), 200
            elif request.json["event"] == "recording.completed":
                mailer.send_recordings_on_recording_completed(request.json)
        return jsonify(""), 200


    @app.route('/alfa_webhook/lesson_changed/', methods=["POST"])  # todo добавить вебхук в альфа
    def alfa_webhook():
        data = request.json
        if is_lesson_conducted(data) and is_lesson_type_eq_group(data):
            lesson_id = data["entity_id"]
            lesson_info = LessonFetcher.by_lesson_id(lesson_id)
            if lesson_info:
                mailer.send_balance(lesson_info)
                mailer.send_reports(lesson_info)
                mailer.send_recordings_on_lesson_held(lesson_info)


    @app.route("/alive")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url=os.getenv("HOST_ROOT") + os.getenv("BOT_TOKEN"))
        return "!", 200


    def is_lesson_conducted(json):
        if json["fields_new"]["status"] == 3:
            return True
        else:
            return False


    def is_lesson_type_eq_group(json):
        if json["fields_rel"]["lesson_type_id"] == 2:
            return True
        else:
            return False


else:
    import tracemalloc
    print("start")
    # clear_all_tables()
    tracemalloc.start()

    test_manager = TestManager(mailer)
    test_manager.execute_auth_all_parents_test(TestMode.MULTY_THREAD)
    test_manager.execute_mailing_tests(TestMode.MULTY_THREAD)


    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"Current memory usage is {current / 10 ** 6}MB; Peak was {peak / 10 ** 6}MB")
    print("end")
    # bot.polling(none_stop=True)

