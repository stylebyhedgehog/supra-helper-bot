from services.api.alfa.group import GroupFetcher
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
        end_date = CgiDataService._get_end_date_of_group_for_months_forming(group_alfa_id)
        data = CgiFetcher.by_group_id(group_alfa_id)
        if data:
            for customer_in_group_info in data:
                if customer_in_group_info.get("customer_id") == child_alfa_id:
                    child_start_studying_in_group_date = DateUtil.normalize_date(customer_in_group_info.get("b_date"))
                    child_start_studying_in_group_date = DateUtil.remove_day(child_start_studying_in_group_date)
                    month_names = DateUtil.generate_month_names(child_start_studying_in_group_date, end_date)
                    return month_names

        Logger.entity_not_found_error("Cgi", group_alfa_id=group_alfa_id, customer_alfa_id=child_alfa_id)
        return None

    @staticmethod
    def _get_end_date_of_group_for_months_forming(group_alfa_id):
        group_data = GroupFetcher.by_id(group_alfa_id)
        if group_data and len(group_data.get("e_date")) > 0:
            current_date_y_m = DateUtil.get_current_moscow_date_y_m_as_str()
            child_end_studying_in_group_date = DateUtil.normalize_date(group_data.get("e_date"))
            child_end_studying_in_group_date_norm = DateUtil.remove_day(child_end_studying_in_group_date)
            if DateUtil.earlier_date(current_date_y_m, child_end_studying_in_group_date_norm) == current_date_y_m: # Если активна
                return DateUtil.get_current_moscow_date_y_m_as_str()
            else:
                return child_end_studying_in_group_date_norm

        return DateUtil.get_current_moscow_date_y_m_as_str()

