from services.api.alfa.template import AlfaApiTemplate
from utils.logger import Logger


class SubjectFetcher:
    @staticmethod
    def all():
        url = "https://supra.s20.online/v2api/subject/index"
        payload = {
            # "id": subject_id,
            "active": False
        }
        # возвращает список всех предметов вопреки параметрам фильтрации
        return AlfaApiTemplate.fetch_paginated_data(url=url, payload=payload)


class SubjectDataService:
    @staticmethod
    def get_subject_name(subject_id):
        subjects = SubjectFetcher.all()
        for subject in subjects:
            if subject.get("id") == subject_id:
                return subject.get("name")
        Logger.entity_not_found_error("Subject (Subject name)", subject_id=subject_id)
        return None
