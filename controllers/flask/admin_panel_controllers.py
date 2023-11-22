from flask import render_template


def register_admin_panel_controllers(app):
    @app.route('/', methods=['GET'])
    def admin_panel():
        return render_template("admin_panel.html")