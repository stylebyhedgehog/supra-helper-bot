from services.api.alfa.template import AlfaApiTemplate
from utils.logger import Logger
from utils.string_utils import StringUtil


class CustomerFetcher:
    @staticmethod
    def all():
        url = "https://supra.s20.online/v2api/customer/index"
        return AlfaApiTemplate.fetch_paginated_data(url=url)

    @staticmethod
    def by_customer_id(customer_id, with_groups=False):
        url = "https://supra.s20.online/v2api/customer/index"
        payload = {"id": customer_id, "withGroups": with_groups, "removed": 1}
        return AlfaApiTemplate.fetch_single_data(url=url, payload=payload)


class CustomerDataService:
    @staticmethod
    def get_customer_groups_by_customer_id(child_alfa_id):
        customer_info = CustomerFetcher.by_customer_id(child_alfa_id, True)
        if customer_info:
            result = []
            for group in customer_info.get("groups"):
                result.append({"id": group.get("id"), "name": group.get("name")})
            if len(result) > 0:
                return result
            else:
                Logger.entity_not_found_error("Customer (Groups)", customer_alfa_id=child_alfa_id)
        else:
            Logger.entity_not_found_error("Customer", customer_alfa_id=child_alfa_id)
            return None

    @staticmethod
    def get_child_balance_by_id(child_alfa_id):
        customer_info = CustomerFetcher.by_customer_id(child_alfa_id)

        if customer_info:
            balance = customer_info.get("balance")
            paid_count = customer_info.get("paid_count")
            name = customer_info.get("name")
            return name, balance, paid_count
        else:
            Logger.entity_not_found_error("Customer (Customer balance)", customer_alfa_id=child_alfa_id)
            return None

    @staticmethod
    def get_child_name_by_id(child_alfa_id):
        customer_info = CustomerFetcher.by_customer_id(child_alfa_id)
        if customer_info:
            name = customer_info.get("name")
            return name
        else:
            Logger.entity_not_found_error("Customer (Customer name)", customer_alfa_id=child_alfa_id)
            return None

    @staticmethod
    def get_customers_by_phone_number(parent_phone_number):
        all_customers = CustomerFetcher.all()
        if all_customers:
            parent_children = []
            for customer in all_customers:
                for phone_number in customer.get("phone", []):
                    normalized_parent_phone_number_from_alfa = StringUtil.remove_brackets_dashes_and_spaces(
                        phone_number)
                    if normalized_parent_phone_number_from_alfa == parent_phone_number:
                        parent_children.append(
                            {"child_id": customer.get("id"),
                             "child_name": customer.get("name"),
                             "parent_name": customer.get("legal_name")})
            if len(parent_children) > 0:
                return parent_children
        else:
            Logger.entity_not_found_error("Customer", parent_phone_number=parent_phone_number)
            return None
