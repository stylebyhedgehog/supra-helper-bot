from datetime import datetime
from services.api.alfa.template import AlfaApiTemplate
from utils.logger import Logger
from utils.date_utils import DateUtil


class CgiFetcher:
    @staticmethod
    def by_group_id(group_id):
        url = "https://supra.s20.online/v2api/cgi/index"
        params = {"group_id": group_id}
        return AlfaApiTemplate.fetch_paginated_data(url=url, params=params)


class CgiDataService:
    @staticmethod
    def get_customer_studying_in_group_months(group_alfa_id, child_alfa_id):
        data = CgiFetcher.by_group_id(group_alfa_id)
        if data:
            for customer_in_group_info in data:
                if customer_in_group_info.get("customer_id") == child_alfa_id:
                    child_start_studying_in_group_date = DateUtil.normalize_date(customer_in_group_info.get("b_date"))
                    child_start_studying_in_group_date = DateUtil.remove_day(child_start_studying_in_group_date)
                    current_date = datetime.now().strftime("%Y-%m")
                    month_names = DateUtil.generate_month_names(child_start_studying_in_group_date, current_date)
                    return month_names

        Logger.entity_not_found_error("Cgi", group_alfa_id=group_alfa_id, customer_alfa_id=child_alfa_id)
        return None
