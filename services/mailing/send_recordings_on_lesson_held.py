import os

from data_storages.db.repositories.absent_child_repository import AbsentChildRepository
from data_storages.db.repositories.lesson_with_absent_child_repository import LessonWithAbsentChildrenRepository
from data_storages.db.repositories.parent_repository import ParentRepository
from services.api.alfa.customer import CustomerDataService
from services.api.alfa.group import GroupDataService
from services.api.alfa.lesson import LessonDataService
from services.api.alfa.room import RoomDataService
from services.api.zoom.recordings import RecordingsDataService, RecordingFetchingStatus
from utils.constants.messages import PPM_ZOOM_RECORDINGS_DISPATCHING
from utils.date_utils import DateUtil
from utils.file_utils import FileUtil
from utils.logger import Logger


class RecordingMailerOnLessonHeld:
    @staticmethod
    def send(bot, lesson_info):
        lesson_id = lesson_info.get("id")
        absent_children = LessonDataService.get_absent_children(lesson_id)

        if absent_children:
            group_id, room_id, start_datetime, lesson_topic = lesson_info.get("group_ids")[0], lesson_info.get("room_id"), \
                                                              lesson_info.get("time_from"), lesson_info.get("topic")

            start_date, start_time = DateUtil.extract_date_and_time(start_datetime)
            group_name = GroupDataService.get_group_name_by_id(group_id)
            utc_lesson_date, utc_lesson_time = DateUtil.moscow_to_utc(start_datetime)
            room_num = RoomDataService.get_room_num_by_id(room_id)

            if room_num is None:
                Logger.mailing_handled_error("mailing_recording_on_lesson_held", f"Room num not specified for lesson with id {lesson_id}")
                return

            resp = RecordingsDataService.by_room_num_group_id_dates_from_to(room_num, group_id, utc_lesson_date, start_time)
            RecordingMailerOnLessonHeld._process_recording(bot, absent_children, resp, lesson_topic,
                                                           group_name, start_date, start_time, room_num,
                                                           group_id, lesson_id)

    @staticmethod
    def _process_recording(bot, absent_children, recording_response, lesson_topic, group_name, start_date, start_time,
                          room_num, group_id, lesson_id):
        if recording_response["status"] == RecordingFetchingStatus.SUCCESS:
            recording_url = recording_response["recording_url"]
            mailing_info = PPM_ZOOM_RECORDINGS_DISPATCHING.RESULT(lesson_topic, recording_url, group_name, start_date, start_time)
            RecordingMailerOnLessonHeld._send_recording_info_to_parents(bot, absent_children, mailing_info)
            RecordingMailerOnLessonHeld._write_in_json_successful_response(absent_children, group_name, lesson_id,
                                                                           lesson_topic, start_date, start_time, mailing_info)
        elif recording_response["status"] == RecordingFetchingStatus.NOT_FOUND:
            RecordingMailerOnLessonHeld._save_absent_children(absent_children, room_num, start_date, start_time, group_id, group_name, lesson_topic,lesson_id)

    @staticmethod
    def _send_recording_info_to_parents(bot, absent_children, recording_info):
        if os.getenv("MAILING_MODE") == 1:
            unique_parents_tg_ids = RecordingMailerOnLessonHeld._get_unique_parents_tg_ids(absent_children)
            for unique_parent_tg_id in unique_parents_tg_ids:
                bot.send_message(unique_parent_tg_id, recording_info)
                Logger.mailing_info(unique_parent_tg_id, "mailing_recording_on_lesson_held", "Successfully mailed")

    @staticmethod
    def _save_absent_children(absent_children, room_num, start_date, start_time, group_id, group_name, lesson_topic, lesson_id):
        LessonWithAbsentChildrenRepository.save(lesson_id, lesson_topic, room_num, start_date, start_time, group_id, group_name)
        for absent_child in absent_children:
            child_id = absent_child.get("child_id")
            child_name = CustomerDataService.get_child_name_by_id(child_id)
            AbsentChildRepository.save(child_id, child_name, lesson_id)

    @staticmethod
    def _write_in_json_successful_response(absent_children, group_name, lesson_id, lesson_topic, start_date, start_time, mailing_info):
        children_info = []
        children_with_parent, children_without_parent = RecordingMailerOnLessonHeld._get_children_with_parent_in_system_and_without(absent_children)

        for child_id in children_with_parent:
            children_info.append({"child_name": CustomerDataService.get_child_name_by_id(child_id),
                                  "status": "Отправлена"})

        for child_id in children_without_parent:
            children_info.append({"child_name": CustomerDataService.get_child_name_by_id(child_id),
                                  "status": "Не отправлена (Отсутствуют зарегистрированные в системе родители)"})

        RecordingMailerOnLessonHeld._write_in_json(group_name, lesson_id, lesson_topic, start_date, start_time, mailing_info, children_info)

        return children_info

    @staticmethod
    def _get_unique_parents_tg_ids(absent_children):
        unique_parents_tg_ids = set()
        for absent_child in absent_children:
            parent = ParentRepository.find_by_child_alfa_id(absent_child.get("child_id"))
            if parent and parent.telegram_id not in unique_parents_tg_ids:
                parent_tg_id = parent.telegram_id
                unique_parents_tg_ids.add(parent_tg_id)
        return unique_parents_tg_ids

    @staticmethod
    def _get_children_with_parent_in_system_and_without(absent_children):
        children_with_parent = []
        children_without_parent = []

        for absent_child in absent_children:
            child_id = absent_child.get("child_id")
            parent = ParentRepository.find_by_child_alfa_id(child_id)
            if parent:
                children_with_parent.append(child_id)
            else:
                children_without_parent.append(child_id)

        return children_with_parent, children_without_parent

    @staticmethod
    def _write_in_json(group_name, lesson_id, lesson_topic, start_date, start_time, mailing_info,
                       children_info):
        try:
            path = FileUtil.get_path_to_mailing_results_file("recordings.json")

            data = {
                "reason_mailing": "Занятие в alfa.crm заполнено",
                "lesson_id": lesson_id,
                "group_name": group_name,
                "lesson_topic": lesson_topic,
                "lesson_datetime": start_date + " " + start_time,
                "mailing_info": mailing_info,
                "mailing_result": children_info
            }
            FileUtil.add_to_json_file(data, path)
        except Exception as e:
            Logger.mailing_handled_error("mailing_recording_on_lesson_held", f"Error on writing in file: {e}")



