from flask import render_template, render_template_string

from exceptions.flask_controller_error_handler import flask_controller_error_handler
from services.dev_service import DevService
from utils.constants.files_names import FN
from utils.file_utils import FileUtil


def register_log_controllers(app):
    @app.route("/logs/info")
    @flask_controller_error_handler
    def info_logs():
        file_path = FileUtil.get_path_to_log_file(FN.LOG_INFO)
        data = FileUtil.read_from_txt_file(file_path)
        return render_template("logs.html", data=data, title="Информационные логи")

    @app.route("/logs/unhandled_errors")
    @flask_controller_error_handler
    def unhandled_errors_logs():
        file_path = FileUtil.get_path_to_log_file(FN.LOG_UNHANDLED_ERRORS)
        data = FileUtil.read_from_txt_file(file_path)
        return render_template("logs.html", data=data, title="Логи необработанных(критических) ошибок")

    @app.route("/logs/handled_errors")
    @flask_controller_error_handler
    def handled_errors_logs():
        file_path = FileUtil.get_path_to_log_file(FN.LOG_HANDLED_ERRORS)
        data = FileUtil.read_from_txt_file(file_path)
        return render_template("logs.html", data=data, title="Логи обработанных ошибок")


    @app.route("/logs/mailing_recording_proces")
    @flask_controller_error_handler
    def mailing_recording_process_logs():
        file_path = FileUtil.get_path_to_log_file(FN.LOG_INFO_RECORDINGS_COMPLETE)
        data = FileUtil.read_from_txt_file(file_path)
        return render_template("logs.html", data=data, title="Логи процесса отправки записей после готовности")

    @app.route("/logs/clone_and_clear")
    @flask_controller_error_handler
    def clone_and_clear_logs():
        res = DevService.clone_and_clear_logs()
        if res:
            return render_template_string("<h1>Для всех logs созданы копии, оригиналы очищены</h1>")
        else:
            return render_template_string("<h1>Ошибка очистки logs, проверьте консоль приложения</h1>")