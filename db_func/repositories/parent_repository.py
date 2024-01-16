from db_func.core import DatabaseManager
from db_func.models import Parent, Child
from db_func.repositories.child_repository import ChildRepository


class ParentRepository:

    @staticmethod
    def save(telegram_id, name, phone_number, telegram_username):
        with DatabaseManager.get_db() as session:
            parent = Parent(telegram_id=telegram_id, name=name, phone_number=phone_number, telegram_username=telegram_username)
            session.add(parent)
            session.commit()
            session.refresh(parent)

            return parent.id

    @staticmethod
    def find_by_telegram_id(telegram_id):
        with DatabaseManager.get_db() as session:
            parent = session.query(Parent).filter_by(telegram_id=telegram_id).first()
            return parent

    @staticmethod
    def find_by_phone_number(phone_number):
        with DatabaseManager.get_db() as session:
            parent = session.query(Parent).filter_by(phone_number=phone_number).first()
            return parent


    @staticmethod
    def find_by_child_alfa_id(child_alfa_id):
        with DatabaseManager.get_db() as session:
            parent = session.query(Parent).join(Child, Parent.id == Child.parent_id) \
                .filter(Child.child_alfa_id == child_alfa_id).first()

            return parent

    @staticmethod
    def find_all():
        with DatabaseManager.get_db() as session:
            parents = session.query(Parent).all()
            return parents

    @staticmethod
    def delete_by_telegram_id(telegram_id):
        with DatabaseManager.get_db() as session:
            parent = session.query(Parent).filter_by(telegram_id=telegram_id).first()

            if parent:
                session.delete(parent)
                session.commit()
                return True
            else:
                return False

    @staticmethod
    def delete_by_id(parent_id):
        with DatabaseManager.get_db() as session:
            parent = session.query(Parent).get(parent_id)

            if parent:
                session.delete(parent)
                session.commit()

                return True
            else:
                return False

    @staticmethod
    def find_all_with_children():
        with DatabaseManager.get_db() as session:
            parents = session.query(Parent).all()
            for parent in parents:
                parent.children = ChildRepository.find_by_parent_id(parent.id)
            return parents