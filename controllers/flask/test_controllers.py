from flask import jsonify

from services.admin_service import clear_all_tables
from tests.tests_manager import TestManager, TestMode
from utils.file_utils import FileUtil


def register_test_controllers(app, mailer):
    @app.route("/start_onethread_tests")
    def start_onethread_tests():
        _clear_files_and_db()
        test_manager = TestManager(mailer)
        test_manager.execute_auth_all_parents_test(TestMode.ONE_THREAD)
        test_manager.execute_mailing_tests(TestMode.ONE_THREAD)


    @app.route("/start_multythread_tests")
    def start_multythread_tests():
        _clear_files_and_db()
        test_manager = TestManager(mailer)
        test_manager.execute_auth_all_parents_test(TestMode.MULTY_THREAD)
        test_manager.execute_mailing_tests(TestMode.MULTY_THREAD)

    @app.route("/clear_all")
    def clear_all():
        _clear_files_and_db()
        return jsonify(""), 200

    def _clear_files_and_db():
        file_path1 = FileUtil.get_path_to_mailing_results_file("recordings.json")
        file_path2 = FileUtil.get_path_to_mailing_results_file("reports.json")
        file_path3 = FileUtil.get_path_to_mailing_results_file("balance.json")
        FileUtil.clear_json(file_path1)
        FileUtil.clear_json(file_path2)
        FileUtil.clear_json(file_path3)
        clear_all_tables()