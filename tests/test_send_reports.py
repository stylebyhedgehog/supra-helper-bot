from services.api.alfa.lesson import LessonFetcher
from services.mailing.send_reports import ReportMailer


def test_send_reports():
    lessons = LessonFetcher.all()
    for lesson in lessons:
        try:
            ReportMailer.send(None, lesson)
        except Exception as e:
            print(f"Ошибка: {e}")