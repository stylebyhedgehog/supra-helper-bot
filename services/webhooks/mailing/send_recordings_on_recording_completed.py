import os

from dotenv import load_dotenv

from db_func.repositories.absent_child_repository import AbsentChildRepository
from db_func.repositories.lesson_with_absent_child_repository import LessonWithAbsentChildrenRepository
from db_func.repositories.parent_repository import ParentRepository
from db_func.repositories.processed_lesson_with_absent_child_repository import \
    ProcessedLessonWithAbsentChildrenRepository
from services.api.alfa.customer import CustomerDataService
from services.api.alfa.lesson import LessonDataService
from utils.constants.files_names import FN
from utils.constants.messages import PPM_ZOOM_RECORDINGS_DISPATCHING
from utils.date_utils import DateUtil
from utils.file_utils import FileUtil
from utils.logger import Logger
from utils.string_utils import StringUtil


class RecordingMailerOnRecordingCompleted:
    @staticmethod
    def send(bot, zoom_json):
        zoom_topic, host_email, start_time, share_url, passcode = RecordingMailerOnRecordingCompleted._extract_zoom_info(zoom_json)
        moscow_date_y_m_d = DateUtil.utc_to_moscow(start_time)
        group_id = StringUtil.extract_number_in_brackets(zoom_topic)
        room_num = StringUtil.extract_number_from_email(host_email)
        potential_lesson_id = RecordingMailerOnRecordingCompleted.get_lesson_id_by_group_id_date_zoom_topic(group_id, moscow_date_y_m_d, zoom_topic)
        Logger.recording_completed_process("Получена запись",
                                           f"Запись с topic: {zoom_topic}. Id подходящего урока: {potential_lesson_id}")

        res = RecordingMailerOnRecordingCompleted._get_lesson_and_absent_children(group_id, room_num, moscow_date_y_m_d, zoom_topic)
        if res:
            lesson, absent_children = res
            recording_url = f"{share_url}?pwd={passcode}"
            Logger.recording_completed_process("Найдено занятие с пропустившими детьми",
                                               f"Запись с topic: {zoom_topic}. Урок с id: {lesson.lesson_id}")
            mailing_info = PPM_ZOOM_RECORDINGS_DISPATCHING.RESULT(lesson.topic, recording_url, lesson.group_name,
                                                                  lesson.start_date,
                                                                  lesson.start_time)
            RecordingMailerOnRecordingCompleted._send_recording_info_to_parents(bot, absent_children, mailing_info, lesson.lesson_id)
            RecordingMailerOnRecordingCompleted._write_in_json_successful_response(absent_children, lesson, mailing_info)
            RecordingMailerOnRecordingCompleted._clear_tables_on_mailed(lesson)

    @staticmethod
    def get_lesson_id_by_group_id_date_zoom_topic(group_id, date, zoom_topic):
        lessons = LessonDataService.get_lesson_by_group_id_date(group_id, date)
        for lesson in lessons:
            date, time = DateUtil.extract_date_and_time(lesson.get("time_from"))
            if time in zoom_topic:
                return lesson.get("id")
        return None


    @staticmethod
    def _clear_tables_on_mailed(lesson):
        ProcessedLessonWithAbsentChildrenRepository.save(lesson.lesson_id, lesson.topic, lesson.room_num,
                                                         lesson.start_date, lesson.start_time, lesson.group_id, lesson.group_name)
        AbsentChildRepository.delete_all_by_lesson_with_absent_child_id(lesson.lesson_id)
        LessonWithAbsentChildrenRepository.delete_by_lesson_id(lesson.lesson_id)


    @staticmethod
    def _send_recording_info_to_parents(bot, absent_children, recording_info, lesson_id):
        if os.getenv("MAILING_MODE") == "1":
            Logger.recording_completed_process("Попытка отправить записи",
                                               f"Урок с id: {lesson_id}")
            unique_parents_tg_ids = RecordingMailerOnRecordingCompleted._get_unique_parents_tg_ids(absent_children)
            for unique_parent_tg_id in unique_parents_tg_ids:
                bot.send_message(unique_parent_tg_id, recording_info)
                Logger.mailing_info(unique_parent_tg_id, "mailing_recording_on_recording_completed", "Successfully mailed")
                Logger.recording_completed_process("Запись отправлена",
                                                   f"Урок с id: {lesson_id}. Родитель: {unique_parent_tg_id}")
    @staticmethod
    def _get_lesson_and_absent_children(group_id, room_num, moscow_date_y_m_d, zoom_topic):
        group_lessons_with_abs_children_on_day = LessonWithAbsentChildrenRepository.find_by_group_id_and_room_num_and_date(
            group_id, room_num,
            moscow_date_y_m_d)
        if group_lessons_with_abs_children_on_day:
            for lesson in group_lessons_with_abs_children_on_day:
                if lesson.start_time in zoom_topic:
                    children = AbsentChildRepository.find_by_lesson_with_absent_children_id(lesson.lesson_id)
                    return lesson, children
        return None

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
            if parent:
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
        payload = zoom_data.get("payload", {})
        object_info = payload.get("object", {})

        topic = object_info.get("topic", "")
        host_email = object_info.get("host_email", "")
        start_time = object_info.get("start_time", "")
        share_url = object_info.get("share_url", "")
        passcode = object_info.get("recording_play_passcode", "")
        return topic, host_email, start_time, share_url, passcode


    @staticmethod
    def _write_in_json(group_name, lesson_id, lesson_topic, start_date, start_time, mailing_info,
                       children_info):
        try:
            path = FileUtil.get_path_to_mailing_results_file(FN.MR_RECORDINGS)

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
            Logger.recording_completed_process("Записано в файл",
                                               f"Урок с id: {lesson_id}")

        except Exception as e:
            Logger.mailing_handled_error("mailing_recording_on_recording_completed", f"Error on writing in file: {e}")

