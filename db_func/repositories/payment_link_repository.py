# payment_link_repository.py
from db_func.core import DatabaseManager
from db_func.models import PaymentLink

class PaymentLinkRepository:
    @staticmethod
    def get_group_payment_link():
        with DatabaseManager.get_db() as session:
            return session.query(PaymentLink).first().group

    @staticmethod
    def get_individual_payment_link():
        with DatabaseManager.get_db() as session:
            return session.query(PaymentLink).first().individual


    @staticmethod
    def update_payment_link_group(group):
        with DatabaseManager.get_db() as session:
            payment_link = session.query(PaymentLink).first()
            if payment_link:
                payment_link.group = group
            else:
                payment_link = PaymentLink(group=group)
                session.add(payment_link)
            session.commit()
            return True

    @staticmethod
    def update_payment_link_individual(individual):
        with DatabaseManager.get_db() as session:
            payment_link = session.query(PaymentLink).first()
            if payment_link:
                payment_link.individual = individual
            else:
                payment_link = PaymentLink(individual=individual)
                session.add(payment_link)
            session.commit()
            return True

