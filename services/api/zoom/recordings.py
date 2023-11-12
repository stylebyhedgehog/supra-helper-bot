from services.api.zoom.template import ZoomApiFetcher
from utils.string_utils import StringUtil


class FetchRecordings:
    @staticmethod
    def by_room_num_from_to(room_num, date_from, date_to):
        url = f"https://api.zoom.us/v2/users/supra.{room_num}@supraschool.ru/recordings"
        params = {"from": date_from, "to": date_to}

        data = ZoomApiFetcher.make_authenticated_request(url=url, params=params)
        return data

    @staticmethod
    def by_room_num_group_id_dates_from_to(room_num, group_alfa_id, date_from, time_start):
        date_to = date_from
        data = FetchRecordings.by_room_num_from_to(room_num, date_from, date_to)
        recording_url = None
        if data:
            meetings = data.get("meetings")
            if len(meetings) > 0:
                for meeting in meetings:
                    topic = meeting.get("topic")
                    if "[" in topic and "]" in topic and group_alfa_id == StringUtil.extract_number_in_brackets(topic) and time_start in topic:
                        share_url = meeting.get("share_url")
                        passcode = meeting.get("recording_play_passcode")
                        access_url = f"{share_url}?pwd={passcode}"
                        recording_url = access_url
                        # recording_id = meeting.get("id")
                        # recording_url = {"access_url":access_url, "recording_id":recording_id}
        return recording_url
