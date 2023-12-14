from flask import render_template_string, render_template

from db_func.core import DatabaseManager
from exceptions.flask_controller_error_handler import flask_controller_error_handler
from services.dev_service import DevService
from tests.tests_manager import TestManager, TestMode


def register_test_controllers(app, mailer):
    @app.route("/start_onethread_tests")
    @flask_controller_error_handler
    def start_onethread_tests():
        _clear_files_and_db()
        test_manager = TestManager(mailer)
        test_manager.execute_auth_all_parents_test(TestMode.ONE_THREAD)
        test_manager.execute_mailing_tests(TestMode.ONE_THREAD)
        return render_template_string("<h1>Однопоточный тест завершен. Пользоватли авторизованы, рассылка имитирована</h1>")


    @app.route("/start_multythread_tests")
    @flask_controller_error_handler
    def start_multythread_tests():
        _clear_files_and_db()
        test_manager = TestManager(mailer)
        test_manager.execute_auth_all_parents_test(TestMode.MULTY_THREAD)
        test_manager.execute_mailing_tests(TestMode.MULTY_THREAD)
        return render_template_string("<h1>Многопоточный тест завершен. Пользоватли авторизованы, рассылка имитирована</h1>")

    @app.route("/clear_db")
    @flask_controller_error_handler
    def clear_db_handler():
        DevService.clear_all_tables()
        return render_template_string("<h1>Вся бд очищена</h1>")

    def _clear_files_and_db():
        DevService.clear_mailing_results()

    @app.route('/show_db')
    def show_all_records():
        try:
            all_records = DatabaseManager.get_all_records()
            return render_template('show_db.html', all_records=all_records)
        except Exception as e:
            return f"Error: {str(e)}"