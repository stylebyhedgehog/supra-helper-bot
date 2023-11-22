from enum import Enum

from tests.bot.test_authenticate_all import AuthenticationTest
from tests.mailing.test_send_balance import MailingBalanceTest
from tests.mailing.test_send_recordings import MailingRecordingsOnLessonHeldTest, MailingRecordingsOnRecordingCompletedTest
from tests.mailing.test_send_reports import MailingReportsTest


class TestManager:
    def __init__(self, mailer):
        self.mailer = mailer

    def execute_auth_all_parents_test(self, mode):
        authentication = AuthenticationTest()
        if mode == TestMode.ONE_THREAD:
            authentication.start_auth_all_parents_test_in_one_thread()
        elif mode == TestMode.MULTY_THREAD:
            authentication.start_auth_all_parents_test_in_multy_threads()

    def execute_mailing_tests(self, mode):
        mailing_balance = MailingBalanceTest(self.mailer)
        mailing_recordings_on_lesson_held = MailingRecordingsOnLessonHeldTest(self.mailer)
        mailing_recordings_on_recording_completed = MailingRecordingsOnRecordingCompletedTest(self.mailer)
        mailing_reports = MailingReportsTest(self.mailer)
        if mode == TestMode.ONE_THREAD:
            mailing_balance.start_test_in_one_thread()
            mailing_recordings_on_lesson_held.start_test_in_one_thread()
            mailing_recordings_on_recording_completed.start_test_in_one_thread()
            mailing_reports.start_test_in_one_thread()
        elif mode == TestMode.MULTY_THREAD:
            mailing_balance.start_test_in_multy_thread()
            mailing_recordings_on_lesson_held.start_test_in_multy_thread()
            mailing_recordings_on_recording_completed.start_test_in_multy_thread()
            mailing_reports.start_test_in_multy_thread()




class TestMode(Enum):
    ONE_THREAD = 1
    MULTY_THREAD = 2
