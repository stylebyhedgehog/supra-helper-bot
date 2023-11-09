from services.api.alfa.lesson import FetchLesson, LessonService
from services.bot.study_results_service import StudyResultsService
from utils.date_utils import DateUtil


class PerformanceService(StudyResultsService):
    @staticmethod
    def get_performance(child_alfa_id, child_group_alfa_id, date_y_m):
        # todo учесть, что у АЯ нет topic_performance
        child_lessons_info = LessonService.get_child_lessons_info(child_alfa_id, child_group_alfa_id, date_y_m)
        if child_lessons_info:
            lessons_amount = len(child_lessons_info)
            summary_grade = StudyResultsService.calculate_summary_grade(child_lessons_info)
            topic_performance = StudyResultsService.form_topic_performance(child_lessons_info)

            average_performance = int(summary_grade / lessons_amount)
            month_name = StudyResultsService.get_month_name(date_y_m)
            return month_name, lessons_amount, average_performance, topic_performance
        return None