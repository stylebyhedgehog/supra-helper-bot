import logging

from services.api.alfa.template import AlfaApiTemplate
from utils.date_utils import DateUtil
from utils.string_utils import StringUtil


class FetchLesson:
    @staticmethod
    def _all():
        url = "https://supra.s20.online/v2api/lesson/index"
        payload = {"date_from": "2023-10-15", "date_to": "2023-11-02"}
        data = AlfaApiTemplate.fetch_paginated_data(url=url, payload=payload)
        return data

    @staticmethod
    def _by_child_id_group_id_period(child_alfa_id, group_alfa_id, date_from, date_to):
        url = "https://supra.s20.online/v2api/lesson/index"
        payload = {"group_id": group_alfa_id, "customer_id": child_alfa_id,
                   "date_from": date_from, "date_to": date_to}
        data = AlfaApiTemplate.fetch_paginated_data(url=url, payload=payload)
        return data

    @staticmethod
    def _by_lesson_id(lesson_id):
        url = "https://supra.s20.online/v2api/lesson/index"
        payload = {"id": lesson_id}
        data = AlfaApiTemplate.fetch_single_data(url=url, payload=payload)
        return data


class LessonService:
    @staticmethod
    def get_child_lessons_info(child_alfa_id, group_alfa_id, date_from):
        lessons = FetchLesson._by_child_id_group_id_period(child_alfa_id, group_alfa_id, date_from,
                                      DateUtil.next_month(date_from))
        result = []
        for lesson in lessons:
            lesson_topic = lesson.get("topic")
            for child_info in lesson.get("details"):
                if child_info.get("customer_id") == child_alfa_id:
                    grade = child_info.get("grade", 0)
                    grade = float(grade.replace(",", "."))
                    child_lesson_info = {
                        "topic": lesson_topic,
                        "is_attend": child_info.get("is_attend"),
                        "grade": grade,
                        "note": child_info.get("note")
                        }
                    result.append(child_lesson_info)
        if len(result) > 0:
            return result
        else:
            logging.error(
                f"Не найдена информация об уроках ребенка с id={child_alfa_id} "
                f"из группы с id={group_alfa_id} за {date_from}")
            return None

    @staticmethod
    def _form_report_body(lessons, child_alfa_id):
        topic_perf_list = []
        teacher_fb = None
        lessons_amount = len(lessons)
        attd_lessons_amount = 0
        summary_grade = 0
        for lesson_info in lessons:
            topic = lesson_info.get("topic")
            for child_info in lesson_info.get("details"):
                if child_info.get("customer_id") == child_alfa_id:
                    is_attend = child_info.get("is_attend")
                    if is_attend == 1:
                        attd_lessons_amount += 1
                        grade = child_info.get("grade")
                        if grade is not None:
                            grade = float(grade.replace(",", "."))
                            topic_perf_list.append(f"{topic} - {grade}%")
                        summary_grade += grade
                    else:
                        topic_perf_list.append(f"{topic} - Пропущено")

                    child_note = child_info.get("note")
                    if StringUtil.is_contain_feedback(child_note):
                        teacher_fb = "Преподаватель отмечает, что " + StringUtil.extract_teacher_feedback(child_note)

        average_attendance = int((attd_lessons_amount / lessons_amount) * 100)
        if attd_lessons_amount > 0:
            average_grade = int(summary_grade / attd_lessons_amount)
        else:
            average_grade = 0
        return topic_perf_list, teacher_fb, lessons_amount, attd_lessons_amount, average_attendance, average_grade





    @staticmethod
    def get_absent_children(lesson_id):
        lesson_info = FetchLesson._by_lesson_id(lesson_id)
        if lesson_info:
            absent_children = []

            for child_info in lesson_info.get("details"):
                if child_info.get("is_attend") == 0:
                    absent_children.append({"child_id": child_info.get("customer_id")})
            if len(absent_children)>0:
                return absent_children
        return None
