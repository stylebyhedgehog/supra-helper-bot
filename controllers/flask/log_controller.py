from flask import render_template, render_template_string

from exceptions.flask_controller_error_handler import flask_controller_error_handler
from services.admin_service import clear_logs
from utils.file_utils import FileUtil


def register_log_controllers(app):
    @app.route("/logs/info")
    @flask_controller_error_handler
    def info_logs():
        file_path = FileUtil.get_path_to_log_file("info.txt")
        data = FileUtil.read_from_txt_file(file_path)
        return render_template("logs.html", data=data, title="Информационные логи")

    @app.route("/logs/unhandled_errors")
    @flask_controller_error_handler
    def unhandled_errors_logs():
        file_path = FileUtil.get_path_to_log_file("unhandled_errors.txt")
        data = FileUtil.read_from_txt_file(file_path)
        return render_template("logs.html", data=data, title="Логи необработанных(критических) ошибок")

    @app.route("/logs/handled_errors")
    @flask_controller_error_handler
    def handled_errors_logs():
        file_path = FileUtil.get_path_to_log_file("handled_errors.txt")
        data = FileUtil.read_from_txt_file(file_path)
        return render_template("logs.html", data=data, title="Логи обработанных ошибок")

    @app.route("/clear_logs")
    @flask_controller_error_handler
    def clear_logs_handler():
        clear_logs()
        return render_template_string("<h1>Все логи очищены</h1>")