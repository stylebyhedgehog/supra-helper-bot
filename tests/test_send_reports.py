from services.api.alfa.lesson import FetchLesson
from services.mailing.send_reports import send_reports


def test_send_reports():
    lessons = FetchLesson._all()
    for lesson in lessons:
        print(lesson.get("id"))
        try:
            send_reports(lesson, None)
        except Exception as e:
            print(f"Ошибка: {e}")