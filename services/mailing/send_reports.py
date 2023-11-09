from db.repositories.parent_repository import ParentRepository
from services.api.alfa.subject import  SubjectService
from services.bot.report_service import ReportService
from tests.utils import TestUtils
from utils.constants.messages import PPM_REPORT_DISPATCHING
from utils.date_utils import DateUtil
from utils.string_utils import StringUtil


def send_reports(lesson_info, bot):
    group_id = lesson_info.get("group_ids")[0]
    date_y_m_d = lesson_info.get("date")
    full_subject_name = SubjectService.get_subject_name(lesson_info.get("subject_id"))
    course_name, subject_name = StringUtil.extract_course_subject(full_subject_name)
    month_name = DateUtil.get_month_name(date_y_m_d)

    children_with_fb = form_list_of_children_with_fb(lesson_info.get("details"))
    for child_with_fb in children_with_fb:
        child_id = child_with_fb["child_id"]
        teacher_fb = child_with_fb["teacher_fb"]
        res = ReportService.form_monthly_report(child_id, group_id, date_y_m_d)
        lessons_amount, attended_lessons_amount, average_attendance, topic_performance = res

        report = _create_notification_message(month_name, lessons_amount, average_attendance,
                                              attended_lessons_amount, teacher_fb, topic_performance,
                                              subject_name, course_name)
        _send_notification_message(child_id, report)


def form_list_of_children_with_fb(lesson_details):
    children = []
    for child_info in lesson_details:
        child_note = child_info.get("note")
        if StringUtil.is_contain_feedback(child_note):
            children.append(
                {"child_id": child_info.get("customer_id"),
                 "teacher_fb": StringUtil.extract_teacher_feedback(child_note)}
            )
    return children


def _create_notification_message(month_name, lessons_amount, average_attendance,
                                 attd_lessons_amount, teacher_fb, topic_perf,
                                 subject_name, course_name):
    report = None
    if course_name == "АЯ":
        report = PPM_REPORT_DISPATCHING.RESULT_EC(month_name, lessons_amount, average_attendance,
                                                  attd_lessons_amount, teacher_fb)
    elif course_name == "КК":
        report = PPM_REPORT_DISPATCHING.RESULT_CC(month_name, lessons_amount, subject_name,
                                                  average_attendance, attd_lessons_amount,
                                                  topic_perf, teacher_fb)
    return report


def _send_notification_message(child_id, report):
    parent = ParentRepository.find_parent_by_child_alfa_id(child_id)
    if parent:
        # bot.send_message(parent.telegram_id, report)
        TestUtils.append_to_file("Отправлен: " + report, "reports.txt")
    else:
        TestUtils.append_to_file("Не отправлен: " + report, "reports.txt")
