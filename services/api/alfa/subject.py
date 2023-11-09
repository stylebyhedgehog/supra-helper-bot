from services.api.alfa.template import AlfaApiTemplate


class FetchSubject:
    @staticmethod
    def all():
        url = "https://supra.s20.online/v2api/subject/index"
        payload = {
            # "id": subject_id,
            "active": False
        }
        # возвращает список всех предметов вопреки параметрам фильтрации
        data = AlfaApiTemplate.fetch_paginated_data(url=url, payload=payload)
        return data


class SubjectService:
    @staticmethod
    def get_subject_name(subject_id):
        subjects = FetchSubject.all()
        if subjects is None:
            return
        for subject in subjects:
            if subject.get("id") == subject_id:
                return subject.get("name")
