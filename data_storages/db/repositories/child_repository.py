import logging

from data_storages.db.core import DatabaseManager
from data_storages.db.models import Child


class ChildRepository:
    @staticmethod
    def save(parent_telegram_id, child_alfa_id, child_name):
        with DatabaseManager.get_db() as session:
            child = Child(parent_telegram_id=parent_telegram_id, child_alfa_id=child_alfa_id,
                          child_name=child_name)
            session.add(child)
            session.commit()

    @staticmethod
    def find_by_parent_telegram_id(parent_telegram_id):
        with DatabaseManager.get_db() as session:
            children = session.query(Child).filter_by(parent_telegram_id=parent_telegram_id).all()
            if children is None or len(children) == 0:
                logging.error(f"Не найдены дети для родителя с tg_id={parent_telegram_id}")
                return None
            return children

    @staticmethod
    def find_all():
        with DatabaseManager.get_db() as session:
            children = session.query(Child).all()
            return children
