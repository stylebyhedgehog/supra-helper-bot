from enum import Enum

from services.api.zoom.template import ZoomApiFetcher
from utils.string_utils import StringUtil


class RecordingsFetcher:
    @staticmethod
    def by_room_num_from_to(room_num, date_from, date_to):
        url = f"https://api.zoom.us/v2/users/supra.{room_num}@supraschool.ru/recordings"
        params = {"from": date_from, "to": date_to}

        return ZoomApiFetcher.make_authenticated_request(url=url, params=params)


class RecordingsDataService:
    @staticmethod
    def by_room_num_group_id_dates_from_to(room_num, group_alfa_id, date_from, time_start):
        date_to = date_from
        data = RecordingsFetcher.by_room_num_from_to(room_num, date_from, date_to)
        if data and len(data.get("meetings")) > 0:
            meetings = data.get("meetings")
            for meeting in meetings:
                topic = meeting.get("topic")
                if StringUtil.contains_group_alfa_id(group_alfa_id, topic):
                    share_url = meeting.get("share_url")
                    passcode = meeting.get("recording_play_passcode")
                    recording_url = f"{share_url}?pwd={passcode}"
                    # Если время соответствует, сразу возвращаем результат
                    if time_start in topic:
                        return {"status": RecordingFetchingStatus.SUCCESS, "recording_url": recording_url}
            # Если время не соответствует
            return {"status": RecordingFetchingStatus.TIME_MISMATCHING, "recording_url": None}
        # Если не найдены записи
        return {"status": RecordingFetchingStatus.NOT_FOUND, "recording_url": None}


class RecordingFetchingStatus(Enum):
    SUCCESS = 1  # Найдены записи для указанного времени, id группы alfa.crm и номера конференции зум
    NOT_FOUND = 2  # Не найдена ни одна запись для указанного id группы alfa.crm
    TIME_MISMATCHING = 3  # Найдены записи для указанной id группы, но время не соответствует
