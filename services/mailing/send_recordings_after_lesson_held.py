from db.repositories.absent_child_repository import AbsentChildRepository
from db.repositories.parent_repository import ParentRepository
from services.api.alfa.group import GroupService
from services.api.alfa.lesson import LessonService
from services.api.alfa.room import RoomService
from services.api.zoom.recordings import FetchRecordings
from tests.utils import TestUtils
from utils.constants.messages import PPM_ZOOM_RECORDINGS_DISPATCHING
from utils.date_utils import DateUtil


def send_recordings_after_lesson_held(lesson, bot):
    lesson_id = lesson.get("id")
    absent_children = LessonService.get_absent_children(lesson_id)
    if absent_children:
        group_id = lesson.get("group_ids")[0]
        room_id = lesson.get("room_id")
        start_datetime = lesson.get("time_from")
        topic = lesson.get("topic")

        start_date, start_time = DateUtil.extract_date_and_time(start_datetime)
        group_name = GroupService.get_group_name_by_id(group_id)
        utc_lesson_date, utc_lesson_time = DateUtil.moscow_to_utc(start_datetime)
        room_num = RoomService.get_room_num_by_id(room_id)
        share_urls = FetchRecordings.by_room_num_group_id_dates_from_to(room_num, group_id, utc_lesson_date,
                                                                        start_time)
        # Если записи найдены/готовы
        if len(share_urls) > 0:
            unique_parent_tg_ids = set()
            for absent_child in absent_children:
                child_id = absent_child.get("child_id")
                parent = ParentRepository.find_parent_by_child_alfa_id(child_id)
                unique_parent_tg_ids.add(parent.telegram_id)

            for unique_parent_tg_id in unique_parent_tg_ids:
                msg = PPM_ZOOM_RECORDINGS_DISPATCHING.RESULT_INLINE_PASSWORD(topic, share_urls, group_name, start_date,
                                                                             start_time)
                # bot.send_message(unique_parent_tg_id, msg)
                TestUtils.append_to_file("Отправлена: " + msg, "recordings.txt")
        # Если записи не найдены/не готовы
        else:
            for absent_child in absent_children:
                child_id = absent_child.get("child_id")
                AbsentChildRepository.save_absent_child(room_num, start_date, start_time, group_id, group_name,
                                                        child_id, topic)
