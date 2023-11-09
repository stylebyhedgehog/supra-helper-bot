from db.core import DatabaseManager
from db.models import Administrator


class AdministratorRepository:

    @staticmethod
    def save_administrator(telegram_id, telegram_username):
        with DatabaseManager.get_db() as session:
            admin = Administrator(telegram_id=telegram_id, telegram_username=telegram_username)
            session.add(admin)
            session.commit()

    @staticmethod
    def find_administrator_by_telegram_id(telegram_id):
        with DatabaseManager.get_db() as session:
            admin = session.query(Administrator).filter_by(telegram_id=telegram_id).first()
            return admin

    @staticmethod
    def find_all_administrators():
        with DatabaseManager.get_db() as session:
            admins = session.query(Administrator).all()
            return admins