from data_storages.db.core import DatabaseManager
from data_storages.db.models import AbsentChild


class AbsentChildRepository:
    @staticmethod
    def save(child_alfa_id, child_name, lesson_with_absent_children_id):
        with DatabaseManager.get_db() as session:
            absent_child = AbsentChild(
                child_alfa_id=child_alfa_id,
                child_name=child_name,
                lesson_with_absent_children_id=lesson_with_absent_children_id,
            )
            session.add(absent_child)
            session.commit()

    @staticmethod
    def find_by_lesson_with_absent_children_id(lesson_with_absent_children_id):
        with DatabaseManager.get_db() as session:
            absent_children = session.query(AbsentChild).filter_by(
                lesson_with_absent_children_id=lesson_with_absent_children_id
            ).all()

            return absent_children

