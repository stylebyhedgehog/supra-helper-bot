from services.api.alfa.template import AlfaApiTemplate
from utils.logger import Logger


class GroupFetcher:
    @staticmethod
    def by_id(group_id):
        url = "https://supra.s20.online/v2api/group/index"
        payload = {"id": group_id, "removed": 3}
        return AlfaApiTemplate.fetch_single_data(url=url, payload=payload)


class GroupDataService:
    @staticmethod
    def get_group_name_by_id(group_id):
        group = GroupFetcher.by_id(group_id)
        if group:
            return group.get("name")
        else:
            Logger.entity_not_found_error("Group (Group name)", alfa_group_id=group_id)
            return None
