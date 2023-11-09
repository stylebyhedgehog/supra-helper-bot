from services.api.alfa.lesson import FetchLesson
from services.mailing.send_balance import send_balance


def test_send_balance():
    lessons = FetchLesson._all()
    for lesson in lessons:
        print(lesson.get("id"))
        send_balance(lesson, None)
