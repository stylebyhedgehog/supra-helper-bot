from flask import render_template

from utils.file_utils import FileUtil


def register_mailing_results_controllers(app):
    @app.route("/mailing_results/balance")
    def mailing_results_balance():
        file_path = FileUtil.get_path_to_mailing_results_file("balance.json")
        data = FileUtil.read_from_json_file(file_path)
        return render_template("balance_mailing_results.html", data=data)

    @app.route("/mailing_results/reports")
    def mailing_results_reports():
        file_path = FileUtil.get_path_to_mailing_results_file("reports.json")
        data = FileUtil.read_from_json_file(file_path)
        return render_template("report_mailing_results.html", data=data)

    @app.route("/mailing_results/recordings")
    def mailing_results_recordings():
        file_path = FileUtil.get_path_to_mailing_results_file("recordings.json")
        data = FileUtil.read_from_json_file(file_path)
        return render_template("recording_mailing_results.html", data=data)
