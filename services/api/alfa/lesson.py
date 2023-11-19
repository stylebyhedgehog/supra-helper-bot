from services.api.alfa.template import AlfaApiTemplate
from utils.logger import Logger
from utils.date_utils import DateUtil


class LessonFetcher:
    @staticmethod
    def all():
        url = "https://supra.s20.online/v2api/lesson/index"
        payload = {"date_from": "2023-11-12", "date_to": "2023-11-20", "lesson_type_id": 2}
        return AlfaApiTemplate.fetch_paginated_data(url=url, payload=payload)

    @staticmethod
    def by_child_id_group_id_period(child_alfa_id, group_alfa_id, date_from, date_to):
        url = "https://supra.s20.online/v2api/lesson/index"
        payload = {"group_id": group_alfa_id, "customer_id": child_alfa_id,
                   "date_from": date_from, "date_to": date_to}
        return AlfaApiTemplate.fetch_paginated_data(url=url, payload=payload)

    @staticmethod
    def by_lesson_id(lesson_id):
        url = "https://supra.s20.online/v2api/lesson/index"
        payload = {"id": lesson_id}
        return AlfaApiTemplate.fetch_single_data(url=url, payload=payload)


class LessonDataService:

    @staticmethod
    def get_child_lessons_info(child_alfa_id, group_alfa_id, date_from):
        lessons = LessonFetcher.by_child_id_group_id_period(child_alfa_id, group_alfa_id, date_from,
                                                            DateUtil.next_month(date_from))
        result = []
        for lesson in lessons:
            lesson_topic = lesson.get("topic")
            for child_info in lesson.get("details"):
                if child_info.get("customer_id") == child_alfa_id:
                    grade = child_info.get("grade", 0)
                    if grade:
                        grade_value = float(grade.replace(",", "."))
                    else:
                        grade_value = 0
                    child_lesson_info = {
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
                                          date_from=date_from)
            return None

    @staticmethod
    def get_absent_children(lesson_id):
        lesson_info = LessonFetcher.by_lesson_id(lesson_id)
        if lesson_info:
            absent_children = []

            for child_info in lesson_info.get("details"):
                if child_info.get("is_attend") == 0:
                    absent_children.append({"child_id": child_info.get("customer_id")})
            if len(absent_children) > 0:
                return absent_children
        return None
