import telebot
from flask import request, jsonify
import os

from services.api.alfa.lesson import LessonFetcher
from utils.encryption import Encryption


def register_external_webhook_controllers(app, bot, mailer):
    @app.route('/tg_webhook/' + os.getenv("BOT_TOKEN"), methods=['POST'])
    def tg_webhook():
        json_str = request.get_data().decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return '', 200

    @app.route("/update_tg_bot_webhook")
    def update_tg_bot_webhook():
        bot.remove_webhook()
        full_url = os.getenv("HOST_ROOT") + "/tg_webhook/" + os.getenv("BOT_TOKEN")
        bot.set_webhook(url=os.getenv("HOST_ROOT") + "/tg_webhook/" + os.getenv("BOT_TOKEN"))
        return f"<h2>Обновленный url вебхука - {full_url}</h2>", 200

    @app.route('/zoom_webhook/recording_completed/', methods=['POST'])
    def zoom_webhook_recording_completed():
        if request.method == "POST":
            if request.json["event"] == "endpoint.url_validation":
                res = Encryption.generate_encrypted_token(request.json, os.getenv("ZOOM_SECRET"))
                return jsonify(res), 200
            elif request.json["event"] == "recording.completed":
                mailer.send_recordings_on_recording_completed(request.json)
        return jsonify(""), 200

    @app.route('/alfa_webhook/lesson_changed/', methods=["POST"])
    def alfa_webhook_lesson_changed():
        data = request.json
        if is_lesson_conducted(data) and is_lesson_type_eq_group(data):
            lesson_id = data["entity_id"]
            lesson_info = LessonFetcher.by_lesson_id(lesson_id)
            if lesson_info:
                mailer.send_balance(lesson_info)
                mailer.send_reports(lesson_info)
                mailer.send_recordings_on_lesson_held(lesson_info)
        return jsonify(""), 200

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
