import telebot
from flask import request, jsonify, render_template_string
import os

from exceptions.flask_controller_error_handler import flask_controller_error_handler
from services.api.alfa.lesson import LessonFetcher
from services.webhooks.participation import ParticipationService
from utils.encryption import Encryption
from utils.file_utils import FileUtil
from utils.logger import Logger


def register_external_webhook_controllers(app, bot, mailer):
    @app.route('/tg_webhook/' + os.getenv("BOT_TOKEN"), methods=['POST'])
    def tg_webhook():
        json_str = request.get_data().decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return '', 200

    @app.route("/update_tg_bot_webhook")
    @flask_controller_error_handler
    def update_tg_bot_webhook():
        bot.remove_webhook()
        full_url = os.getenv("HOST_ROOT") + "/tg_webhook/" + os.getenv("BOT_TOKEN")
        bot.set_webhook(url=os.getenv("HOST_ROOT") + "/tg_webhook/" + os.getenv("BOT_TOKEN"))
        return render_template_string(f"<h2>Обновленный url вебхука - {full_url}</h2>")

    @app.route('/zoom_webhook/recording_completed/', methods=['POST'])
    def zoom_webhook_recording_completed():
        if request.method == "POST":
            if request.json["event"] == "endpoint.url_validation":
                Logger.webhook_call_info("Zoom", "zoom_webhook_recording_completed", "zoom validation", "Zoom request for validation")
                res = Encryption.generate_encrypted_token(request.json, os.getenv("ZOOM_SECRET"))
                return jsonify(res), 200
            elif request.json["event"] == "recording.completed":
                object_id = request.json.get('payload').get('object').get('id')
                object_topic = request.json.get('payload').get('object').get('topic')
                Logger.webhook_call_info("Zoom", "zoom_webhook_recording_completed", "recording completed",
                                         f"Zoom request with recording data. Id: {object_id}, Meeting Topic: {object_topic}")
                mailer.send_recordings_on_recording_completed(request.json)
        return jsonify(""), 200

    @app.route('/alfa_webhook/lesson_changed', methods=["POST"])
    def alfa_webhook_lesson_changed():
        data = request.json
        if is_lesson_conducted(data) and is_lesson_type_eq_group(data):
            lesson_id = data["entity_id"]
            Logger.webhook_call_info("Alfa.crm", "alfa_webhook_lesson_changed", "lesson conducted",
                                     f"Alfa.crm request with lesson data. Lesson id: {lesson_id}")
            lesson_info = LessonFetcher.by_lesson_id(lesson_id)
            if lesson_info:
                mailer.send_balance_on_expiration(lesson_info)
                mailer.send_reports(lesson_info)
                mailer.send_recordings_on_lesson_held(lesson_info)
        return jsonify(""), 200

    @app.route('/alfa_webhook/participation', methods=["POST"])
    def alfa_webhook_participation():
        data = request.json
        path = FileUtil.get_path_to_mailing_results_file("temp_on_participation.json")
        FileUtil.add_to_json_file(data, path)
        if data.get("event") == "create":
            group_id = data.get("fields_new").get("group_id")
            customer_id = data.get("fields_new").get("customer_id")
            Logger.webhook_call_info("Alfa.crm", "alfa_webhook_participation", "child joined group",
                                     f"Alfa.crm request with customer_id: {customer_id}, group_id: {group_id}")
            ParticipationService.create_and_attach_to_parent_new_child(customer_id, group_id)
        return jsonify(""), 200

    @app.route('/alfa_webhook/payment', methods=["POST"])
    def alfa_webhook_payment():
        data = request.json
        path = FileUtil.get_path_to_mailing_results_file("temp_on_payment.json")
        FileUtil.add_to_json_file(data, path)
        if data.get("event") == "create":
            customer_id = data.get("fields_new").get("customer_id")
            mailer.send_balance_on_payment(customer_id)
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
