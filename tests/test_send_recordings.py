from services.api.alfa.lesson import LessonFetcher
from services.mailing.send_recordings_on_lesson_held import send_recordings_after_lesson_held
from services.mailing.send_recordings_on_recording_completed import send_recordings_after_recording_completed


def test_send_recordings_on_lesson_held():
    lessons = LessonFetcher.all()
    for lesson in lessons:
        print(lesson.get("id"))
        try:
            send_recordings_after_lesson_held(lesson, None)
        except Exception as e:
            print(f"Ошибка: {e}")


def test_send_recordings_on_recording_complete():
    json = get_test_json()
    send_recordings_after_recording_completed(json, None)


def get_test_json():
    return {
        "payload": {
            "account_id": "n9D1u_kRQhe-GBbRTpT4mQ",
            "object": {
                "uuid": "LjtP8z2jS0qmRJIIb1WuBg==",
                "id": 85392858403,
                "account_id": "n9D1u_kRQhe-GBbRTpT4mQ",
                "host_id": "c7qNTbLwTU6CzokdhwEjkg",
                "topic": "Unity_4 зум 18:40 [142]",
                "type": 8,
                "start_time": "2023-11-03T16:59:56Z",
                "timezone": "Europe/Moscow",
                "host_email": "supra.12@supraschool.ru",
                "duration": 67,
                "total_size": 310615812,
                "recording_count": 4,
                "share_url": "https://us06web.zoom.us/rec/share/xl01l7Ye0ciA93a0nYBr8oeVi2icYQ6NBn75B8E4Tsvse8bnJKMPo-HxDDsw5cAm.Tn29FVLGeuRgnJZX",
                "recording_files": [
                    {
                        "id": "9ef4fc58-bb36-4726-a476-50599513d6e5",
                        "meeting_id": "LjtP8z2jS0qmRJIIb1WuBg==",
                        "recording_start": "2023-11-16T16:59:57Z",
                        "recording_end": "2023-11-16T18:07:05Z",
                        "file_type": "M4A",
                        "file_extension": "M4A",
                        "file_size": 64090363,
                        "play_url": "https://us06web.zoom.us/rec/play/wEfnY6Q75yY4gwQh9C6d0Ew6sYa3okG_RO07ObZnn3LcEfcAeWIdYlpP-J95YICuMQ9sCccaLr5pd99W.FFYfPPmRn1Y70noP",
                        "download_url": "https://us06web.zoom.us/rec/webhook_download/wEfnY6Q75yY4gwQh9C6d0Ew6sYa3okG_RO07ObZnn3LcEfcAeWIdYlpP-J95YICuMQ9sCccaLr5pd99W.FFYfPPmRn1Y70noP/If4839jJLKdcInLgoD9TIOTmv5hljoR_Q-RfPZwP5hLtrw5GDehmbPGvb-otaUwsPw.QImvuIPX4Ckwh7i7",
                        "status": "completed",
                        "recording_type": "audio_only"
                    },
                    {
                        "id": "58dae725-86b7-4432-9233-f4d0c55edb07",
                        "meeting_id": "LjtP8z2jS0qmRJIIb1WuBg==",
                        "recording_start": "2023-11-16T16:59:57Z",
                        "recording_end": "2023-11-16T18:07:05Z",
                        "file_type": "TIMELINE",
                        "file_extension": "JSON",
                        "file_size": 686420,
                        "download_url": "https://us06web.zoom.us/rec/webhook_download/LXMSKYb6VFJw2IKGEj70VoM-xvf5733OUuT4hpa_v6ZAaPOZRRy6mxZ685iLf0LnJqGinPqnHmpX6jRQ.h-y4QjabTeGUYAsQ/ETZyiN-2zTS7FkojOffuEBlhRIeaCYFhrAan-sO69TclInTXI8f8DG7DuiLq-ojn9TMH9VqX.Lnff-RbEanRVWAbO",
                        "status": "completed",
                        "recording_type": "timeline"
                    },
                    {
                        "id": "b23dfe73-89b0-4680-b650-83cfb253ca1f",
                        "meeting_id": "LjtP8z2jS0qmRJIIb1WuBg==",
                        "recording_start": "2023-11-16T16:59:57Z",
                        "recording_end": "2023-11-16T18:07:05Z",
                        "file_type": "CHAT",
                        "file_extension": "TXT",
                        "file_size": 360,
                        "play_url": "https://us06web.zoom.us/rec/play/AszQ5Lc8PzcrLx3ZdMSpI09V1VAhnx7OGvKDSAYDoO_bipe-aTqui7x6YgaKQxeMWKTraOj0rCET52Y.akO7Evka7vSSaqmv",
                        "download_url": "https://us06web.zoom.us/rec/webhook_download/AszQ5Lc8PzcrLx3ZdMSpI09V1VAhnx7OGvKDSAYDoO_bipe-aTqui7x6YgaKQxeMWKTraOj0rCET52Y.akO7Evka7vSSaqmv/3YIQr_gjWNOzGFPw-BzSv73M3uxblhAQL9OkDk5rFRsnSRHHd34YNUu0vVXfTWyKB7U.ACSTbe-eS9_niqZl",
                        "status": "completed",
                        "recording_type": "chat_file"
                    },
                    {
                        "id": "e508e251-4530-4020-ad19-5dfdc8777391",
                        "meeting_id": "LjtP8z2jS0qmRJIIb1WuBg==",
                        "recording_start": "2023-11-16T16:59:57Z",
                        "recording_end": "2023-11-16T18:07:05Z",
                        "file_type": "MP4",
                        "file_extension": "MP4",
                        "file_size": 245838669,
                        "play_url": "https://us06web.zoom.us/rec/play/aHB4HnLl90zRJHYHZguCj-jLBfI630CbXmcDrrL_lY8vv7Libkc957VQBmBXRHdoWw9A9sZUBFg2l2CG.MTbpF5F2dBfZUI5H",
                        "download_url": "https://us06web.zoom.us/rec/webhook_download/aHB4HnLl90zRJHYHZguCj-jLBfI630CbXmcDrrL_lY8vv7Libkc957VQBmBXRHdoWw9A9sZUBFg2l2CG.MTbpF5F2dBfZUI5H/_St2t2ZhVBxi76AjmJfWctEF9_8ae7AuMFpjxntNT85Ir12nasKOXRhNo1Tp898Fwg.GEouq_B12lsHmLcz",
                        "status": "completed",
                        "recording_type": "shared_screen_with_speaker_view"
                    }
                ],
                "password": "9$If6&tn",
                "recording_play_passcode": "yGfvDEpWE3NvnBEtc3JXf15tvWsgoOoD",
                "on_prem": False
            }
        },
        "event_ts": 1700160240202,
        "event": "recording.completed",
        "download_token": "eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJodHRwczovL2V2ZW50Lnpvb20udXMiLCJhY2NvdW50SWQiOiJuOUQxdV9rUlFoZS1HQmJSVHBUNG1RIiwiYXVkIjoiaHR0cHM6Ly9vYXV0aC56b29tLnVzIiwibWlkIjoiTGp0UDh6MmpTMHFtUkpJSWIxV3VCZz09IiwiZXhwIjoxNzAwMjQ2NjU1LCJ1c2VySWQiOiJjN3FOVGJMd1RVNkN6b2tkaHdFamtnIn0.ptMuRTBS417TqUCyZTCPG-Bq4omMrNqpgt6J46zYOuIARoCtkPaNNlQl2bF2e6JnvUgDS8dTBHz7McwF5ofFSw"
    }