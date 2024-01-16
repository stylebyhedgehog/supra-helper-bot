from flask import Flask, render_template, request, redirect, url_for, jsonify
from db_func.models import Parent, Child
from db_func.repositories.child_repository import ChildRepository
from db_func.repositories.parent_repository import ParentRepository


# Главная страница
from exceptions.flask_controller_error_handler import flask_controller_error_handler
from services.bot.authentication_service import AuthenticationService


def register_parent_controller(app):
    @app.route('/parent', methods=["GET", "POST"])
    @flask_controller_error_handler
    def parent_manipulations_main():
        if request.method == 'POST':
            telegram_id = int(request.form['telegram_id'])
            telegram_username = request.form['telegram_username']
            phone_number = request.form['phone_number']

            if not telegram_username:
                telegram_username = None

            res = AuthenticationService.authorize_parent(phone_number, telegram_id, telegram_username)
            if not res:
                return f"Ошибка при добавлении родителя с telegram_id={telegram_id}, phone_number={phone_number},telegram_username={telegram_username}", 404


        parents = ParentRepository.find_all_with_children()
        return render_template('parent_manipulations_main.html', parents=parents)

    # Страница для удаления родителя
    @app.route('/delete_parent/<string:id>', methods=['GET'])
    @flask_controller_error_handler
    def delete_parent(id):
        id = int(id)
        success_children = ChildRepository.delete_by_parent_id(id)
        success_parent = ParentRepository.delete_by_id(id)
        if success_children and success_parent:
            return redirect(url_for('parent_manipulations_main'))
        else:
            return f"Ошибка при удалении родителя с id={id}", 404

    @app.route('/get_children/<int:parent_id>')
    @flask_controller_error_handler
    def get_children(parent_id):
        children = ChildRepository.find_by_parent_id(parent_id)
        children_list = [{'child_name': child.child_name, 'child_alfa_id': child.child_alfa_id} for child in children]
        return jsonify(children_list)


