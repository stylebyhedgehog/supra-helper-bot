from services.api.alfa.group import GroupDataService
from services.api.alfa.lesson import LessonFetcher
from services.api.alfa.room import RoomDataService
from services.api.zoom.recordings import RecordingsDataService, RecordingFetchingStatus
from utils.date_utils import DateUtil


class RecordingsService:
    @staticmethod
    def get_recording_by_lesson_id(lesson_id):
        lesson = LessonFetcher.by_lesson_id(lesson_id)
        if lesson:
            group_id, room_id, start_datetime, lesson_topic = lesson.get("group_ids")[0], lesson.get("room_id"),\
                                                              lesson.get("time_from"), lesson.get("topic")
            start_date, start_time = DateUtil.extract_date_and_time(start_datetime)
            group_name = GroupDataService.get_group_name_by_id(group_id)
            utc_lesson_date, utc_lesson_time = DateUtil.moscow_to_utc(start_datetime)
            room_num = RoomDataService.get_room_num_by_id(room_id)

            if room_num is None:
                return None

            resp = RecordingsDataService.by_room_num_group_id_dates_from_to(room_num, group_id, utc_lesson_date, start_time)

            if resp["status"] == RecordingFetchingStatus.SUCCESS:
                recording_url = resp["recording_url"]
                datetime = start_date + " " + start_time
                return recording_url, group_name, datetime, lesson_topic
            elif resp["status"] == RecordingFetchingStatus.NOT_FOUND:
                return None
        return None