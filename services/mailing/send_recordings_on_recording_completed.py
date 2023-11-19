import logging
import os

from data_storages.db.repositories.absent_child_repository import AbsentChildRepository
from data_storages.db.repositories.lesson_with_absent_child_repository import LessonWithAbsentChildrenRepository
from data_storages.db.repositories.parent_repository import ParentRepository
from services.api.alfa.customer import CustomerDataService
from utils.constants.messages import PPM_ZOOM_RECORDINGS_DISPATCHING
from utils.date_utils import DateUtil
from utils.file_utils import FileUtil
from utils.string_utils import StringUtil


class RecordingMailerOnRecordingCompleted:
    @staticmethod
    def send(bot, zoom_json):
        zoom_topic, host_email, start_time, share_url, passcode = RecordingMailerOnRecordingCompleted._extract_zoom_info(zoom_json)
        moscow_date_y_m_d = DateUtil.utc_to_moscow(start_time)
        group_id = StringUtil.extract_number_in_brackets(zoom_topic)
        room_num = StringUtil.extract_number_from_email(host_email)
        lesson, absent_children = RecordingMailerOnRecordingCompleted._get_lesson_and_absent_children(group_id, room_num, moscow_date_y_m_d, zoom_topic)

        recording_url = f"{share_url}?pwd={passcode}"
        mailing_info = PPM_ZOOM_RECORDINGS_DISPATCHING.RESULT(lesson.topic, recording_url, lesson.group_name,
                                                              lesson.start_date,
                                                              lesson.start_time)
        RecordingMailerOnRecordingCompleted._send_recording_info_to_parents(bot, absent_children, mailing_info)
        RecordingMailerOnRecordingCompleted._write_in_json_successful_response(absent_children, lesson, mailing_info)
        LessonWithAbsentChildrenRepository.delete_by_lesson_id(lesson.lesson_id)

    @staticmethod
    def _send_recording_info_to_parents(bot, absent_children, recording_info):
        if os.getenv("MAILING_MODE") == 1:
            unique_parents_tg_ids = RecordingMailerOnRecordingCompleted._get_unique_parents_tg_ids(absent_children)
            for unique_parent_tg_id in unique_parents_tg_ids:
                bot.send_message(unique_parent_tg_id, recording_info)

    @staticmethod
    def _get_lesson_and_absent_children(group_id, room_num, moscow_date_y_m_d, zoom_topic):
        group_lessons_with_abs_children_on_day = LessonWithAbsentChildrenRepository.find_by_group_id_and_room_num_and_date(
            group_id, room_num,
            moscow_date_y_m_d)
        for lesson in group_lessons_with_abs_children_on_day:
            if lesson.start_time in zoom_topic:
                children = AbsentChildRepository.find_by_lesson_with_absent_children_id(lesson.lesson_id)
                return lesson, children

    @staticmethod
    def _write_in_json_successful_response(absent_children, lesson, mailing_info):
        children_info = []
        children_with_parent, children_without_parent = RecordingMailerOnRecordingCompleted._get_children_with_parent_in_system_and_without(absent_children)

        for child_id in children_with_parent:
            children_info.append({"child_name": CustomerDataService.get_child_name_by_id(child_id),
                                  "status": "Отправлена"})

        for child_id in children_without_parent:
            children_info.append({"child_name": CustomerDataService.get_child_name_by_id(child_id),
                                  "status": "Не отправлена (Отсутствуют зарегистрированные в системе родители)"})

        RecordingMailerOnRecordingCompleted._write_in_json(lesson.group_name, lesson.lesson_id, lesson.topic, lesson.start_date, lesson.start_time,
                       mailing_info, children_info)

        return children_info

    @staticmethod
    def _get_unique_parents_tg_ids(absent_children):
        unique_parents_tg_ids = set()
        for absent_child in absent_children:
            parent = ParentRepository.find_by_child_alfa_id(absent_child.child_alfa_id)
            if parent and parent.telegram_id not in unique_parents_tg_ids:
                parent_tg_id = parent.telegram_id
                unique_parents_tg_ids.add(parent_tg_id)
        return unique_parents_tg_ids

    @staticmethod
    def _get_children_with_parent_in_system_and_without(absent_children):
        children_with_parent = []
        children_without_parent = []

        for absent_child in absent_children:
            child_id = absent_child.child_alfa_id
            parent = ParentRepository.find_by_child_alfa_id(child_id)
            if parent:
                children_with_parent.append(child_id)
            else:
                children_without_parent.append(child_id)

        return children_with_parent, children_without_parent

    @staticmethod
    def _extract_zoom_info(zoom_data):
        try:
            payload = zoom_data.get("payload", {})
            object_info = payload.get("object", {})

            topic = object_info.get("topic", "")
            host_email = object_info.get("host_email", "")
            start_time = object_info.get("start_time", "")
            share_url = object_info.get("share_url", "")
            passcode = object_info.get("recording_play_passcode", "")
            return topic, host_email, start_time, share_url, passcode

        except Exception as e:
            print(f"Error extracting Zoom info: {str(e)}")
            return None, None, None, None, None

    @staticmethod
    def _write_in_json(group_name, lesson_id, lesson_topic, start_date, start_time, mailing_info,
                       children_info):
        try:
            path = FileUtil.get_path_to_mailing_results_file("recordings.json")

            data = {
                "reason_mailing": "Запись zoom готова",
                "lesson_id": lesson_id,
                "group_name": group_name,
                "lesson_topic": lesson_topic,
                "lesson_datetime": start_date + " " + start_time,
                "mailing_info": mailing_info,
                "mailing_result": children_info
            }
            FileUtil.add_to_json_file(data, path)
        except Exception as e:
            logging.error(f"Ошибка записи информации о записях в файл {e}")
