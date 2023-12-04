from utils.date_utils import DateUtil


class StudyResultsService:
    @staticmethod
    def calculate_attended_lessons_amount(child_lessons_info):
        return sum(child_lesson_info.get("is_attend") for child_lesson_info in child_lessons_info)

    @staticmethod
    def calculate_summary_grade(child_lessons_info):
        return sum(child_lesson_info.get("grade") for child_lesson_info in child_lessons_info)

    @staticmethod
    def get_month_name(date_y_m):
        return DateUtil.get_month_name(date_y_m)

    @staticmethod
    def form_topic_performance(child_lessons_info):
        topic_performance = ""
        for child_lesson_info in child_lessons_info:
            is_attend = child_lesson_info.get("is_attend")
            date = child_lesson_info.get("date")
            grade = child_lesson_info.get("grade")
            topic = child_lesson_info.get("topic")
            if is_attend:
                topic_performance += f"\n ▪{date} {topic} - {grade}%"
            else:
                topic_performance += f"\n ▪{date} {topic} - Пропущено"
        return topic_performance