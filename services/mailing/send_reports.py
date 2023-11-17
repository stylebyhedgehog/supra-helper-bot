import logging

from db.repositories.parent_repository import ParentRepository
from services.api.alfa.customer import CustomerDataService
from services.api.alfa.group import GroupDataService
from services.bot.report_service import ReportService
from utils.date_utils import DateUtil
from utils.file_utils import FileUtil
from utils.string_utils import StringUtil


def send_reports(lesson_info, bot):
    children_on_lesson = lesson_info.get("details")
    # Отчеты отправляются только в случае наличия ос у всех детей на уроке
    if _is_fb_present_for_all_children(children_on_lesson):
        group_id = lesson_info.get("group_ids")[0]
        date_y_m_d = lesson_info.get("date")
        date_y_m = DateUtil.remove_day(date_y_m_d)
        subject_id = lesson_info.get("subject_id")

        reports_containers = ReportService.get_monthly_reports(group_id, date_y_m, subject_id, children_on_lesson)
        for report_container in reports_containers:
            child_id = report_container.get("child_id")
            parent = ParentRepository.find_by_child_alfa_id(child_id)
            # _send_notification_message(parent, report, bot)
            _write_in_json(report_container,parent)


def _is_fb_present_for_all_children(children_on_lesson):
    for child_on_lesson in children_on_lesson:
        if not StringUtil.is_contain_feedback(child_on_lesson.get("note")):
            return False
    return True

def _write_in_json(report_container,parent):
    try:
        path = FileUtil.get_path_to_tmp_json_file("reports.json")

        status = "Не отправлен (Родитель не зарегистрирован в системе)"
        if parent:
            status = "Отправлен"
        data = {
            "group_name": GroupDataService.get_group_name_by_id(report_container.get("group_id")),
            "child_name": CustomerDataService.get_child_name_by_id(report_container.get("child_id")),
            "month_name": report_container.get("month_name"),
            "report": report_container.get("report"),
            "status": status
        }
        FileUtil.add_to_json_file(data,path)
    except Exception as e:
        logging.error(f"Ошибка записи отчета в файл {e}")

def _send_notification_message(parent, info, bot):
    if parent:
        bot.send_message(parent.telegram_id, info)

