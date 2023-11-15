from services.api.alfa.lesson import LessonFetcher
from services.mailing.send_balance import send_balance


def test_send_balance():
    lessons = LessonFetcher.all()
    for lesson in lessons:
        try:
            send_balance(lesson, None)
        except Exception as e:
            print(f"Ошибка: {e}")
