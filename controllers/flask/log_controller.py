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


    @app.route("/logs/clone_and_clear")
    @flask_controller_error_handler
    def clone_and_clear_logs():
        res = DevService.clone_and_clear_logs()
        if res:
            return render_template_string("<h1>Для всех logs созданы копии, оригиналы очищены</h1>")
        else:
            return render_template_string("<h1>Ошибка очистки logs, проверьте консоль приложения</h1>")

    @app.route("/logs/info_deprecated")
    @flask_controller_error_handler
    def info_logs_deprecated():
        file_path = FileUtil.get_path_to_log_file(FN.LOG_INFO_DEPRECATED)
        data = FileUtil.read_from_txt_file(file_path)
        last_modified = FileUtil.get_file_last_modified_time(file_path)
        return render_template("logs.html", data=data, title=f"Устаревшие Информационные логи (Копия создана: {last_modified})")

    @app.route("/logs/unhandled_errors_deprecated")
    @flask_controller_error_handler
    def unhandled_errors_logs_deprecated():
        file_path = FileUtil.get_path_to_log_file(FN.LOG_UNHANDLED_ERRORS_DEPRECATED)
        data = FileUtil.read_from_txt_file(file_path)
        last_modified = FileUtil.get_file_last_modified_time(file_path)
        return render_template("logs.html", data=data, title=f"Устаревшие Логи необработанных(критических) ошибок (Копия создана: {last_modified})")

    @app.route("/logs/handled_errors_deprecated")
    @flask_controller_error_handler
    def handled_errors_logs_deprecated():
        file_path = FileUtil.get_path_to_log_file(FN.LOG_HANDLED_ERRORS_DEPRECATED)
        data = FileUtil.read_from_txt_file(file_path)
        last_modified = FileUtil.get_file_last_modified_time(file_path)
        return render_template("logs.html", data=data, title=f"Устаревшие Логи обработанных ошибок (Копия создана: {last_modified})")

