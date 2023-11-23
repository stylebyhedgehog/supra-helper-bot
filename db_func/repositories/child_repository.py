from db_func.core import DatabaseManager
from db_func.models import Child, Parent


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

    @staticmethod
    def delete_by_parent_tg_id(parent_telegram_id):
        with DatabaseManager.get_db() as session:
            parent = session.query(Parent).filter_by(telegram_id=parent_telegram_id).first()

            if parent:
                children = session.query(Child).filter_by(parent_id=parent.id).all()
                for child in children:
                    session.delete(child)

                session.commit()

                return True
            else:
                return False