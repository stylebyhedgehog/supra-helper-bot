import logging

from dotenv import load_dotenv
import telebot
from flask import Flask, request, jsonify
import os

from controllers.bot.admin.authed_parents_list_handlers import register_get_authed_parents_list
from controllers.bot.menu_handlers import register_menu_handlers
from controllers.bot.parent.attendance_handlers import register_child_get_attendance_handlers
from controllers.bot.parent.authenication_handlers import register_authorization_handlers
from controllers.bot.parent.balance_handlers import register_child_get_balance
from controllers.bot.parent.contact_administrator_handler import register_contact_administrator
from controllers.bot.parent.performance_handlers import register_child_get_performance_handlers

from db.core import DatabaseManager
from services.admin_service import clear_all_tables
from services.api.alfa.lesson import LessonFetcher, LessonDataService
from services.api.alfa.template import AlfaApiTemplate
from services.mailing.send_balance import send_balance
from services.mailing.send_recordings_after_lesson_held import send_recordings_after_lesson_held
from services.mailing.send_recordings_after_recording_completed import send_recordings_after_recording_completed
from services.mailing.send_reports import send_reports
from tests.test_authenticate_all import authenticate_all
from tests.test_send_balance import test_send_balance
from tests.test_send_recordings import test_send_recordings
from tests.test_send_reports import test_send_reports
from utils.encryption import Encryption
from utils.file_utils import FileUtil



load_dotenv()
# todo реализовать отлавливание изменения состава групп
DatabaseManager.init_db('sqlite:///' + FileUtil.get_path_to_db())
app = Flask(__name__)
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"), threaded=False)


register_menu_handlers(bot)
register_authorization_handlers(bot)
register_contact_administrator(bot)
register_get_authed_parents_list(bot)
register_child_get_performance_handlers(bot)
register_child_get_attendance_handlers(bot)
register_child_get_balance(bot)

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
                send_recordings_after_recording_completed(request.json, bot)
        return jsonify(""), 200


    @app.route('/alfa_webhook/lesson_changed/', methods=["POST"])  # todo добавить вебхук в альфа
    def alfa_webhook():
        data = request.json
        if is_lesson_conducted(data) and is_lesson_type_eq_group(data):
            lesson_id = data["entity_id"]
            lesson_info = LessonFetcher.by_lesson_id(lesson_id)
            if lesson_info:
                send_balance(lesson_info, bot)
                send_reports(lesson_info, bot)
                send_recordings_after_lesson_held(lesson_info, bot)


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
    tracemalloc.start()
    # authenticate_all()
    # test_send_balance()
    test_send_recordings()
    # test_send_reports()

    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage is {current / 10 ** 6}MB; Peak was {peak / 10 ** 6}MB")
    tracemalloc.stop()
    print("end")
    # bot.polling(none_stop=True)

