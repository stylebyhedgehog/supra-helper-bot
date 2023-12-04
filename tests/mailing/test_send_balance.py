from tests.mailing.test_mailing import MailingTest


class MailingBalanceTest(MailingTest):
    def _threadable_task(self, mailer, lesson):
        mailer.send_balance_on_expiration(lesson)
        print(lesson)

