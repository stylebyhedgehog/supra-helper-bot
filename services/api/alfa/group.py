import logging
from services.api.alfa.template import AlfaApiTemplate


class FetchGroup:
    @staticmethod
    def by_id(group_id):
        url = "https://supra.s20.online/v2api/group/index"
        payload = {"id": group_id, "removed": 3}
        data = AlfaApiTemplate.fetch_single_data(url=url, payload=payload)
        return data


class GroupService:
    @staticmethod
    def get_group_name_by_id(group_id):
        group = FetchGroup.by_id(group_id)
        if group:
            return group.get("name")
        else:
            logging.error(f"Не найдена группа с id={group_id}")
            return None
