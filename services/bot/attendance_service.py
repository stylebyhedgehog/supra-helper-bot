import logging

from services.api.alfa.lesson import LessonService
from services.bot.study_results_service import StudyResultsService


class AttendanceService(StudyResultsService):

    @staticmethod
    def get_attendance(child_alfa_id, child_group_alfa_id, date_y_m):
        child_lessons_info = LessonService.get_child_lessons_info(child_alfa_id, child_group_alfa_id, date_y_m)
        if child_lessons_info:
            lessons_amount = len(child_lessons_info)
            attended_lessons_amount = StudyResultsService.calculate_attended_lessons_amount(child_lessons_info)
            average_attendance = int((attended_lessons_amount / lessons_amount) * 100)
            return lessons_amount, attended_lessons_amount, average_attendance
        return None
