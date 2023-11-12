import logging

from db.repositories.absent_child_repository import AbsentChildRepository
from db.repositories.parent_repository import ParentRepository
from services.api.alfa.customer import CustomerDataService
from services.api.alfa.group import GroupDataService
from services.api.alfa.lesson import LessonDataService
from services.api.alfa.room import RoomDataService
from services.api.zoom.recordings import FetchRecordings
from utils.constants.messages import PPM_ZOOM_RECORDINGS_DISPATCHING
from utils.date_utils import DateUtil
from utils.file_utils import FileUtil


def send_recordings_after_lesson_held(lesson, bot):
    lesson_id = lesson.get("id")
    absent_children = LessonDataService.get_absent_children(lesson_id)
    if absent_children:
        group_id = lesson.get("group_ids")[0]
        room_id = lesson.get("room_id")
        start_datetime = lesson.get("time_from")
        topic = lesson.get("topic")

        start_date, start_time = DateUtil.extract_date_and_time(start_datetime)
        group_name = GroupDataService.get_group_name_by_id(group_id)
        utc_lesson_date, utc_lesson_time = DateUtil.moscow_to_utc(start_datetime)
        room_num = RoomDataService.get_room_num_by_id(room_id)
        share_url = FetchRecordings.by_room_num_group_id_dates_from_to(room_num, group_id, utc_lesson_date,
                                                                        start_time)
        print(share_url)
        # Если записи найдены/готовы
        if share_url:
            parent_children, children_without_parents = _form_parent_absent_children_dict(absent_children)
            for unique_parent_tg_id, children_ids in parent_children.items():
                msg = PPM_ZOOM_RECORDINGS_DISPATCHING.RESULT_INLINE_PASSWORD(topic, share_url, group_name, start_date,
                                                                             start_time)
                # _send_notification_message(unique_parent_tg_id, msg, bot)
                for child_id in children_ids:
                    _write_in_json(topic,group_name, start_date, start_time, child_id, share_url, "Отправлена")
            for child_without_parent_in_system in children_without_parents:
                _write_in_json(topic, group_name, start_date, start_time, child_without_parent_in_system, share_url, "Не отправлен (Родитель не зарегистрирован в системе)")
        # Если записи не найдены/не готовы
        else:
            for absent_child in absent_children:
                child_id = absent_child.get("child_id")
                AbsentChildRepository.save_absent_child(room_num, start_date, start_time, group_id, group_name,
                                                        child_id, topic)


def _form_parent_absent_children_dict(absent_children):
    parent_children = {}
    children_without_parents = []
    for absent_child in absent_children:
        child_id = absent_child.get("child_id")
        parent = ParentRepository.find_parent_by_child_alfa_id(child_id)
        if parent:
            parent_tg_id = parent.telegram_id
            if parent_tg_id not in parent_children.keys():
                parent_children[parent_tg_id] = [child_id]
            else:
                parent_children[parent_tg_id].append(child_id)
        else:
            children_without_parents.append(child_id)
    return parent_children, children_without_parents


def _write_in_json(topic,group_name, start_date, start_time, child_id, share_url, status):
    try:
        path = FileUtil.get_path_to_tmp_json_file("recordings_after_lesson_held.json")

        data = {
            "group_name": group_name,
            "topic": topic,
            "child_name": CustomerDataService.get_child_name_by_id(child_id),
            "datetime": start_date + " " + start_time,
            "recording_url": share_url,
            "status": status
        }
        FileUtil.add_to_json_file(data, path)
    except Exception as e:
        logging.error(f"Ошибка записи информации о записях в файл {e}")


def _send_notification_message(parent_tg_id, info, bot):
    bot.send_message(parent_tg_id, info)

