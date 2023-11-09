from db.core import DatabaseManager
from db.models import AbsentChild


class AbsentChildRepository:
    @staticmethod
    def save_absent_child(room_num, start_date, start_time, group_alfa_id,group_alfa_name, child_alfa_id,  topic):
        with DatabaseManager.get_db() as session:
            absent_child = AbsentChild(room_num=room_num, start_date=start_date, start_time=start_time,
                                       group_alfa_id=group_alfa_id, child_alfa_id=child_alfa_id,
                                       group_alfa_name=group_alfa_name, topic=topic)
            session.add(absent_child)
            session.commit()

    @staticmethod
    def find_absent_children_by_group_id_and_room_num_and_date(group_id, room_num, date):
        with DatabaseManager.get_db() as session:
            absent_children = session.query(AbsentChild).filter(
                AbsentChild.group_alfa_id == group_id,
                AbsentChild.room_num == room_num,
                AbsentChild.start_date == date
            ).all()

            return absent_children

    @staticmethod
    def delete_absent_child_by_id(id):
        with DatabaseManager.get_db() as session:
            absent_child = session.query(AbsentChild).filter(AbsentChild.id == id).first()

            if absent_child:
                session.delete(absent_child)
                session.commit()
                return True
            else:
                return False