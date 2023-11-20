import threading

from services.api.alfa.lesson import LessonFetcher


class MailingTest:
    def __init__(self, mailer):
        self.mailer = mailer

    def _threadable_task(self, mailer, data):
        pass

    def _prepare_test_input_data_list(self):
        lessons = LessonFetcher.all()
        results = [lesson for lesson in lessons]
        return results

    def start_test_in_one_thread(self):
        input_test_data_list = self._prepare_test_input_data_list()
        mailer = self.mailer
        for input_test_data in input_test_data_list:
            self._threadable_task(mailer, input_test_data)

    def start_test_in_multy_thread(self):
        input_test_data_list = self._prepare_test_input_data_list()
        mailer = self.mailer
        threads = []

        for input_test_data in input_test_data_list:
            thread = threading.Thread(target=self._threadable_task, args=(mailer, input_test_data,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()