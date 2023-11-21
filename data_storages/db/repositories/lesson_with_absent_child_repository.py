from data_storages.db.core import DatabaseManager
from data_storages.db.models import LessonWithAbsentChildren


class LessonWithAbsentChildrenRepository:
    @staticmethod
    def save(lesson_id, topic, room_num, start_date, start_time, group_id, group_name):
        with DatabaseManager.get_db() as session:
            lesson = LessonWithAbsentChildren(
                lesson_id=lesson_id,
                topic=topic,
                room_num=room_num,
                start_date=start_date,
                start_time=start_time,
                group_id=group_id,
                group_name=group_name,
            )
            session.add(lesson)
            session.commit()

    @staticmethod
    def delete_by_lesson_id(lesson_id):
        with DatabaseManager.get_db() as session:
            lesson = session.query(LessonWithAbsentChildren).filter_by(lesson_id=lesson_id).first()
            if lesson:
                session.delete(lesson)
                session.commit()

    @staticmethod
    def find_by_group_id_and_room_num_and_date(group_id, room_num, date):
        with DatabaseManager.get_db() as session:
            lessons = session.query(LessonWithAbsentChildren).filter(
                LessonWithAbsentChildren.group_id == group_id,
                LessonWithAbsentChildren.room_num == room_num,
                LessonWithAbsentChildren.start_date == date
            ).all()

            return lessons


    @staticmethod
    def find_all():
        with DatabaseManager.get_db() as session:
            lessons = session.query(LessonWithAbsentChildren).all()
            return lessons