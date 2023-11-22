import random

from data_storages.db.repositories.lesson_with_absent_child_repository import LessonWithAbsentChildrenRepository
from tests.mailing.test_mailing import MailingTest
from utils.date_utils import DateUtil


class MailingRecordingsOnLessonHeldTest(MailingTest):
    def _threadable_task(self, mailer, lesson):
        mailer.send_recordings_on_lesson_held(lesson)
        print(lesson)


class MailingRecordingsOnRecordingCompletedTest(MailingTest):
    #todo не работает корректно
    def _threadable_task(self, mailer, json):
        mailer.send_recordings_on_recording_completed(json)
        print(json)

    def _prepare_test_input_data_list(self):
        test_list = []
        lessons = LessonWithAbsentChildrenRepository.find_all()
        for lesson in lessons:
            test_json = self._form_test_recording_json(lesson)
            test_list.append(test_json)
        return test_list

    def _form_test_recording_json(self, lesson):
        seconds = str(random.randint(1, 50))
        utc_date, utc_time = DateUtil.moscow_to_utc(lesson.start_date + " " + lesson.start_time+f":{seconds}")
        utc_datetime = f"{utc_date}T{utc_time}:{seconds}Z"
        return {
            "payload": {
                "account_id": "n9D1u_kRQhe-GBbRTpT4mQ",
                "object": {
                    "uuid": "LjtP8z2jS0qmRJIIb1WuBg==",
                    "id": 85392858403,
                    "account_id": "n9D1u_kRQhe-GBbRTpT4mQ",
                    "host_id": "c7qNTbLwTU6CzokdhwEjkg",
                    "topic": f"{lesson.group_name} зум {lesson.start_time} [{lesson.group_id}]",
                    "type": 8,
                    "start_time": utc_datetime,
                    "timezone": "Europe/Moscow",
                    "host_email": f"supra.{lesson.room_num}@supraschool.ru",
                    "duration": 67,
                    "total_size": 310615812,
                    "recording_count": 4,
                    "share_url": f"generated_url_for_{lesson.group_name}",
                    "recording_files": [
                        {}
                    ],
                    "password": "9$If6&tn",
                    "recording_play_passcode": f"generated_passcode",
                    "on_prem": False
                }
            },
            "event_ts": 1700160240202,
            "event": "recording.completed",
            "download_token": "eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJodHRwczovL2V2ZW50Lnpvb20udXMiLCJhY2NvdW50SWQiOiJuOUQxdV9rUlFoZS1HQmJSVHBUNG1RIiwiYXVkIjoiaHR0cHM6Ly9vYXV0aC56b29tLnVzIiwibWlkIjoiTGp0UDh6MmpTMHFtUkpJSWIxV3VCZz09IiwiZXhwIjoxNzAwMjQ2NjU1LCJ1c2VySWQiOiJjN3FOVGJMd1RVNkN6b2tkaHdFamtnIn0.ptMuRTBS417TqUCyZTCPG-Bq4omMrNqpgt6J46zYOuIARoCtkPaNNlQl2bF2e6JnvUgDS8dTBHz7McwF5ofFSw"
        }
