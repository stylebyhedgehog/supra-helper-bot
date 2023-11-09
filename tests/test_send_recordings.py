from services.api.alfa.lesson import FetchLesson
from services.mailing.send_recordings_after_lesson_held import send_recordings_after_lesson_held


def test_send_recordings():
    lessons = FetchLesson._all()
    for lesson in lessons:
        print(lesson.get("id"))
        try:
            send_recordings_after_lesson_held(lesson, None)
        except Exception as e:
            print(f"Ошибка: {e}")