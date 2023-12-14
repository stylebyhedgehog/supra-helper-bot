from flask import render_template, jsonify, render_template_string

from exceptions.flask_controller_error_handler import flask_controller_error_handler
from services.dev_service import DevService
from utils.constants.files_names import FN
from utils.file_utils import FileUtil


def register_mailing_results_controllers(app):
    @app.route("/mailing_results/balance")
    @flask_controller_error_handler
    def mailing_results_balance():
        file_path = FileUtil.get_path_to_mailing_results_file(FN.MR_BALANCE)
        data = FileUtil.read_from_json_file(file_path)
        return render_template("balance_mailing_results.html", data=data)

    @app.route("/mailing_results/reports")
    @flask_controller_error_handler
    def mailing_results_reports():
        file_path = FileUtil.get_path_to_mailing_results_file(FN.MR_REPORTS)
        data = FileUtil.read_from_json_file(file_path)
        return render_template("report_mailing_results.html", data=data)

    @app.route("/mailing_results/recordings")
    @flask_controller_error_handler
    def mailing_results_recordings():
        file_path = FileUtil.get_path_to_mailing_results_file(FN.MR_RECORDINGS)
        data = FileUtil.read_from_json_file(file_path)
        return render_template("recording_mailing_results.html", data=data)


    @app.route("/mailing_results/payment")
    @flask_controller_error_handler
    def mailing_results_payment():
        file_path = FileUtil.get_path_to_mailing_results_file(FN.MR_TEMP_ON_PAYMENT)
        data = FileUtil.read_from_json_file(file_path)
        return jsonify(data), 200

    @app.route("/mailing_results/participation")
    @flask_controller_error_handler
    def mailing_results_participation():
        file_path = FileUtil.get_path_to_mailing_results_file(FN.MR_TEMP_ON_PARTICIPATION)
        data = FileUtil.read_from_json_file(file_path)
        return jsonify(data), 200


    @app.route("/mailing_results/clone_and_clear")
    @flask_controller_error_handler
    def clone_and_clear_mailing_results():
        res = DevService.clone_and_clear_mailing_results()
        if res:
            return render_template_string("<h1>Для всех mailing_results созданы копии, оригиналы очищены</h1>")
        else:
            return render_template_string("<h1>Ошибка очистки logs, проверьте консоль приложения</h1>")
