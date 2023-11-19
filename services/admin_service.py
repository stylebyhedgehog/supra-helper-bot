from data_storages.db.core import DatabaseManager
from data_storages.db.models import Child, AbsentChild, Parent, Administrator, LessonWithAbsentChildren


def clear_all_tables():
    with DatabaseManager.get_db() as session:
        session.query(Child).delete()
        session.query(LessonWithAbsentChildren).delete()
        session.query(AbsentChild).delete()
        session.query(Parent).delete()
        session.query(Administrator).delete()
        session.commit()
