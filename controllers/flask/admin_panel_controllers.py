from flask import render_template

from exceptions.flask_controller_error_handler import flask_controller_error_handler
from utils.file_utils import FileUtil


def register_admin_panel_controllers(app):

    @app.route('/', methods=['GET'])
    @flask_controller_error_handler
    def admin_panel():
        res = FileUtil.get_data_size()
        return render_template("admin_panel.html", size=res)
