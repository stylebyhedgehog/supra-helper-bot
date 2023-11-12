from services.api.alfa.lesson import LessonDataService
from services.api.alfa.subject import SubjectDataService
from services.bot.study_results_service import StudyResultsService
from utils.constants.messages import PPM_REPORT_DISPATCHING
from utils.date_utils import DateUtil
from utils.string_utils import StringUtil


class ReportService(StudyResultsService):

    @staticmethod
    def get_monthly_reports(group_id, date_y_m, subject_id, children_on_lesson):
        full_subject_name = SubjectDataService.get_subject_name(subject_id)
        course_name, subject_name = StringUtil.extract_course_subject(full_subject_name)
        month_name = DateUtil.get_month_name(date_y_m)
        reports_containers = []
        for child_on_lesson in children_on_lesson:
            child_id = child_on_lesson.get("customer_id")
            teacher_fb = StringUtil.extract_teacher_feedback(child_on_lesson.get("note"))
            report = ReportService._form_report(child_id, group_id, date_y_m, month_name, teacher_fb, subject_name,
                                                course_name)
            reports_containers.append(
                {"group_id": group_id, "child_id": child_id, "month_name": month_name, "report": report})
        return reports_containers
    @staticmethod
    def _form_report(child_id, group_id, date_y_m,
                     month_name, teacher_fb,
                     subject_name, course_name):

        report = None
        if course_name == "АЯ":
            res = ReportService._form_monthly_report_body_for_ec(child_id, group_id, date_y_m)
            lessons_amount, attended_lessons_amount, average_attendance = res
            report = PPM_REPORT_DISPATCHING.RESULT_EC(month_name, lessons_amount, average_attendance,
                                                      attended_lessons_amount, teacher_fb)
        elif course_name == "КК":
            res = ReportService._form_report_body_for_cc(child_id, group_id, date_y_m)
            lessons_amount, attended_lessons_amount, average_attendance, topic_performance = res
            report = PPM_REPORT_DISPATCHING.RESULT_CC(month_name, lessons_amount, subject_name,
                                                      average_attendance, attended_lessons_amount,
                                                      topic_performance, teacher_fb)
        return report

    @staticmethod
    def _form_report_body_for_cc(child_alfa_id, child_group_alfa_id, date_y_m):
        child_lessons_info = LessonDataService.get_child_lessons_info(child_alfa_id, child_group_alfa_id, date_y_m)

        lessons_amount = len(child_lessons_info)
        attended_lessons_amount = StudyResultsService.calculate_attended_lessons_amount(child_lessons_info)
        average_attendance = int((attended_lessons_amount / lessons_amount) * 100)
        topic_performance = StudyResultsService.form_topic_performance(child_lessons_info)

        return lessons_amount, attended_lessons_amount, average_attendance, topic_performance

    @staticmethod
    def _form_monthly_report_body_for_ec(child_alfa_id, child_group_alfa_id, date_y_m):
        child_lessons_info = LessonDataService.get_child_lessons_info(child_alfa_id, child_group_alfa_id, date_y_m)

        lessons_amount = len(child_lessons_info)
        attended_lessons_amount = StudyResultsService.calculate_attended_lessons_amount(child_lessons_info)
        average_attendance = int((attended_lessons_amount / lessons_amount) * 100)

        return lessons_amount, attended_lessons_amount, average_attendance

    # @staticmethod
    # def _form_list_of_children_with_fb(lesson_details):
    #     children = []
    #     for child_info in lesson_details:
    #         child_note = child_info.get("note")
    #         if StringUtil.is_contain_feedback(child_note):
    #             children.append(
    #                 {"child_id": child_info.get("customer_id"),
    #                  "teacher_fb": StringUtil.extract_teacher_feedback(child_note)}
    #             )
    #     return children
