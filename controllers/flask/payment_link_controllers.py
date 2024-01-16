from flask import request, redirect, url_for, render_template

from db_func.repositories.payment_link_repository import PaymentLinkRepository
from exceptions.flask_controller_error_handler import flask_controller_error_handler


def register_payment_link_controllers(app):
    def render_payment_links_page():
        group_link = PaymentLinkRepository.get_group_payment_link()
        individual_link = PaymentLinkRepository.get_individual_payment_link()
        return render_template('payment_links.html', group_link=group_link, individual_link=individual_link)

    @app.route('/payment_links', methods=['GET'])
    @flask_controller_error_handler
    def display_payment_links():
        return render_payment_links_page()

    @app.route('/payment_links/group_link', methods=['POST'])
    @flask_controller_error_handler
    def update_group_link():
        group = request.form['group']
        success_group = PaymentLinkRepository.update_payment_link_group(group)

        if success_group:
            return redirect(url_for('display_payment_links'))
        else:
            return "Error updating group link", 500

    @app.route('/payment_links/individual_link', methods=['POST'])
    @flask_controller_error_handler
    def update_individual_link():
        individual = request.form['individual']
        success_individual = PaymentLinkRepository.update_payment_link_individual(individual)

        if success_individual:
            return redirect(url_for('display_payment_links'))
        else:
            return "Error updating individual link", 500
