import logging

from data_storages.db.core import DatabaseManager
from data_storages.db.models import Child, Parent


class ChildRepository:
    @staticmethod
    def save(parent_id, child_alfa_id, child_name):
        with DatabaseManager.get_db() as session:
            child = Child(parent_id=parent_id, child_alfa_id=child_alfa_id,
                          child_name=child_name)
            session.add(child)
            session.commit()

    @staticmethod
    def find_by_parent_telegram_id(parent_telegram_id):
        with DatabaseManager.get_db() as session:
            parent = session.query(Parent).filter_by(telegram_id=parent_telegram_id).first()
            if parent:
                children = session.query(Child).filter_by(parent_id=parent.id).all()
                return children
            else:
                return None

    @staticmethod
    def find_all():
        with DatabaseManager.get_db() as session:
            children = session.query(Child).all()
            return children
