from db.core import DatabaseManager
from db.models import Child, AbsentChild, Parent, Administrator


def clear_all_tables():
    with DatabaseManager.get_db() as session:
        session.query(Child).delete()
        session.query(AbsentChild).delete()
        session.query(Parent).delete()
        session.query(Administrator).delete()
        session.commit()
