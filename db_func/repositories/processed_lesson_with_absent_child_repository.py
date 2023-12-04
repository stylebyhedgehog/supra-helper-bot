from db_func.core import DatabaseManager
from db_func.models import  ProcessedLessonWithAbsentChildren


class ProcessedLessonWithAbsentChildrenRepository:
    @staticmethod
    def save(lesson_id, topic, room_num, start_date, start_time, group_id, group_name):

        with DatabaseManager.get_db() as session:
            lesson = ProcessedLessonWithAbsentChildren(
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

