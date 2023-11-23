from tests.mailing.test_mailing import MailingTest


class MailingReportsTest(MailingTest):
    def _threadable_task(self, mailer, lesson):
        mailer.send_reports(lesson)
        print(lesson)
