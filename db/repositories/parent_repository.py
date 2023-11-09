from db.core import DatabaseManager
from db.models import Parent, Child


class ParentRepository:

    @staticmethod
    def save_parent(telegram_id, name, phone_number):
        with DatabaseManager.get_db() as session:
            parent = Parent(telegram_id=telegram_id, name=name, phone_number=phone_number)
            session.add(parent)
            session.commit()

    @staticmethod
    def find_parent_by_telegram_id(telegram_id):
        with DatabaseManager.get_db() as session:
            parent = session.query(Parent).filter_by(telegram_id=telegram_id).first()
            return parent

    @staticmethod
    def find_parent_by_child_alfa_id(child_alfa_id):
        with DatabaseManager.get_db() as session:
            parent = session.query(Parent).join(Child, Parent.telegram_id == Child.parent_telegram_id) \
                .filter(Child.child_alfa_id == child_alfa_id).first()

            return parent

    @staticmethod
    def find_all_parents():
        with DatabaseManager.get_db() as session:
            parents = session.query(Parent).all()
            return parents