import threading

from services.api.alfa.lesson import LessonFetcher
from services.mailing.mailer import Mailer


def test_send_balance_in_one_thread():
    lessons = LessonFetcher.all()
    results = []
    for lesson in lessons:
        results.append(lesson)
    mailer = Mailer(None)

    for result in results:
        print(result)
        mailer.send_balance(result)


def threadable_task(mailer, lesson):
    mailer.send_balance(lesson)
    print(lesson)


def test_send_balance_in_multy_thread():
    lessons = LessonFetcher.all()
    results = []
    for lesson in lessons:
        results.append(lesson)

    mailer = Mailer(None)
    threads = []
    for result in results:

        thread = threading.Thread(target=threadable_task, args=(mailer, result,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()