from services.api.alfa.lesson import LessonService
from services.bot.study_results_service import StudyResultsService
from utils.date_utils import DateUtil


class ReportService(StudyResultsService):

    @staticmethod
    def form_monthly_report(child_alfa_id, child_group_alfa_id, date_y_m_d):
        date_y_m = DateUtil.remove_day(date_y_m_d)
        child_lessons_info = LessonService.get_child_lessons_info(child_alfa_id, child_group_alfa_id, date_y_m)

        lessons_amount = len(child_lessons_info)
        attended_lessons_amount = StudyResultsService.calculate_attended_lessons_amount(child_lessons_info)
        average_attendance = int((attended_lessons_amount/lessons_amount)*100)
        topic_performance = StudyResultsService.form_topic_performance(child_lessons_info)

        return lessons_amount, attended_lessons_amount, average_attendance, topic_performance

