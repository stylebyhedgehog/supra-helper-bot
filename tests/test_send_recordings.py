from services.api.alfa.lesson import LessonFetcher
from services.mailing.send_recordings_after_lesson_held import send_recordings_after_lesson_held


def test_send_recordings():
    lessons = LessonFetcher.all()
    for lesson in lessons:
        print(lesson.get("id"))
        try:
            send_recordings_after_lesson_held(lesson, None)
        except Exception as e:
            print(f"Ошибка: {e}")
