from exceptions.mailing_error_handler import mailing_error_handler
from services.mailing.send_balance import BalanceMailer
from services.mailing.send_recordings_on_lesson_held import RecordingMailerOnLessonHeld
from services.mailing.send_recordings_on_recording_completed import RecordingMailerOnRecordingCompleted
from services.mailing.send_reports import ReportMailer


class Mailer:
    def __init__(self, bot):
        self.bot = bot

    @mailing_error_handler
    def send_balance(self, lesson_info):
        BalanceMailer.send(self.bot, lesson_info)

    @mailing_error_handler
    def send_recordings_on_lesson_held(self, lesson_info):
        RecordingMailerOnLessonHeld.send(self.bot, lesson_info)

    @mailing_error_handler
    def send_recordings_on_recording_completed(self, zoom_json):
        RecordingMailerOnRecordingCompleted.send(self.bot, zoom_json)

    @mailing_error_handler
    def send_reports(self, lesson_info):
        ReportMailer.send(self.bot, lesson_info)
