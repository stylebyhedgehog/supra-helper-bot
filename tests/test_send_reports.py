from services.api.alfa.lesson import LessonFetcher
from services.mailing.send_reports import send_reports


def test_send_reports():
    lessons = LessonFetcher._all()
    for lesson in lessons:
        try:
            send_reports(lesson, None)
        except Exception as e:
            print(f"Ошибка: {e}")