from flask import render_template

from exceptions.flask_controller_error_handler import flask_controller_error_handler


def register_admin_panel_controllers(app):

    @app.route('/', methods=['GET'])
    @flask_controller_error_handler
    def admin_panel():
        return render_template("admin_panel.html")