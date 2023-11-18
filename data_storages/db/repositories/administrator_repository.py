from data_storages.db.core import DatabaseManager
from data_storages.db.models import Administrator


class AdministratorRepository:

    @staticmethod
    def save(telegram_id, telegram_username):
        with DatabaseManager.get_db() as session:
            admin = Administrator(telegram_id=telegram_id, telegram_username=telegram_username)
            session.add(admin)
            session.commit()

    @staticmethod
    def find_by_telegram_id(telegram_id):
        with DatabaseManager.get_db() as session:
            admin = session.query(Administrator).filter_by(telegram_id=telegram_id).first()
            return admin

    @staticmethod
    def find_all():
        with DatabaseManager.get_db() as session:
            admins = session.query(Administrator).all()
            return admins