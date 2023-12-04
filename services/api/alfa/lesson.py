from services.api.alfa.template import AlfaApiTemplate
from utils.logger import Logger
from utils.date_utils import DateUtil


class LessonFetcher:
    @staticmethod
    def all():
        url = "https://supra.s20.online/v2api/lesson/index"
        payload = {"date_from": "2023-10-25", "date_to": "2023-11-20", "lesson_type_id": 2}
        return AlfaApiTemplate.fetch_paginated_data(url=url, payload=payload)

    @staticmethod
    def by_child_id_group_id_period(child_alfa_id, group_alfa_id, date_from, date_to):
        url = "https://supra.s20.online/v2api/lesson/index"
        payload = {"group_id": group_alfa_id, "customer_id": child_alfa_id,
                   "date_from": date_from, "date_to": date_to}
        return AlfaApiTemplate.fetch_paginated_data(url=url, payload=payload)

    @staticmethod
    def by_group_id_date(group_alfa_id, date):
        url = "https://supra.s20.online/v2api/lesson/index"
        payload = {"group_id": group_alfa_id,
                   "date_from": date, "date_to": date}
        return AlfaApiTemplate.fetch_paginated_data(url=url, payload=payload)

    @staticmethod
    def by_lesson_id(lesson_id):
        url = "https://supra.s20.online/v2api/lesson/index"
        payload = {"id": lesson_id}
        return AlfaApiTemplate.fetch_single_data(url=url, payload=payload)

    @staticmethod
    def last_by_group_id(group_alfa_id):
        url = "https://supra.s20.online/v2api/lesson/index"
        payload = {"group_id": group_alfa_id}
        return AlfaApiTemplate.fetch_single_data(url=url, payload=payload)

class LessonDataService:
    @staticmethod
    def get_lesson_by_group_id_date(group_id, date):
        return LessonFetcher.by_group_id_date(group_id, date)
    @staticmethod
    def get_child_lessons_info_for_week(child_alfa_id, group_alfa_id):
        last_week_date_str, current_date_str = DateUtil.get_date_week_ago_and_current()
        lessons = LessonFetcher.by_child_id_group_id_period(child_alfa_id, group_alfa_id, last_week_date_str, current_date_str)
        result = []
        for lesson in lessons:
            lesson_topic = lesson.get("topic")
            lesson_date = lesson.get("date")
            lesson_id = lesson.get("id")
            for child_info in lesson.get("details"):
                if child_info.get("customer_id") == child_alfa_id:
                    child_lesson_info = {
                        "id": lesson_id,
                        "date": lesson_date,
                        "topic": lesson_topic
                    }
                    result.append(child_lesson_info)
        if len(result) > 0:
            return result
        else:
            Logger.entity_not_found_error("Lesson (Study Results)", alfa_child_id=child_alfa_id, alfa_group_id=group_alfa_id)
            return None

    @staticmethod
    def get_child_lessons_info_for_month(child_alfa_id, group_alfa_id, date_y_m):
        lessons = LessonFetcher.by_child_id_group_id_period(child_alfa_id, group_alfa_id, date_y_m,
                                                            DateUtil.next_month(date_y_m))
        result = []
        for lesson in lessons:
            lesson_topic = lesson.get("topic")
            lesson_date = lesson.get("date")
            for child_info in lesson.get("details"):
                if child_info.get("customer_id") == child_alfa_id:
                    grade = child_info.get("grade", 0)
                    if grade:
                        grade_value = float(grade.replace(",", "."))
                    else:
                        grade_value = 0
                    child_lesson_info = {
                        "date": lesson_date,
                        "topic": lesson_topic,
                        "is_attend": child_info.get("is_attend"),
                        "grade": grade_value,
                        "note": child_info.get("note")
                    }
                    result.append(child_lesson_info)
        if len(result) > 0:
            return result
        else:
            Logger.entity_not_found_error("Lesson (Study Results)", alfa_child_id=child_alfa_id, alfa_group_id=group_alfa_id,
                                          date_y_m=date_y_m)
            return None

    @staticmethod
    def get_absent_children(lesson_id):
        lesson_info = LessonFetcher.by_lesson_id(lesson_id)
        if lesson_info:
            absent_children = []

            for child_info in lesson_info.get("details"):
                # Считаем, что клиенты с заморзкой не пропустили занятие
                if child_info.get("is_attend") == 0 and child_info.get("reason_id") != 7:
                    absent_children.append({"child_id": child_info.get("customer_id")})
            if len(absent_children) > 0:
                return absent_children
        return None

    @staticmethod
    def get_subject_id_by_group_id(group_id):
        lesson = LessonFetcher.last_by_group_id(group_id)
        if lesson:
            return lesson.get("subject_id")
        return None