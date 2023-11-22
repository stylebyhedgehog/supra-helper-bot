from services.api.alfa.lesson import LessonDataService
from services.bot.study_results_service import StudyResultsService


class PerformanceService(StudyResultsService):
    @staticmethod
    def get_performance(child_alfa_id, child_group_alfa_id, date_y_m):
        child_lessons_info = LessonDataService.get_child_lessons_info(child_alfa_id, child_group_alfa_id, date_y_m)
        if child_lessons_info:
            lessons_amount = len(child_lessons_info)
            summary_grade = StudyResultsService.calculate_summary_grade(child_lessons_info)
            attended_lessons_amount = StudyResultsService.calculate_attended_lessons_amount(child_lessons_info)

            if attended_lessons_amount !=0:
                average_performance = int(summary_grade / attended_lessons_amount)
            else:
                average_performance = 0
            month_name = StudyResultsService.get_month_name(date_y_m)

            topic_performance = StudyResultsService.form_topic_performance(child_lessons_info)
            return month_name, lessons_amount, average_performance, topic_performance
        return None
