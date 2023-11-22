import os
import threading

from data_storages.db.repositories.administrator_repository import AdministratorRepository
from data_storages.db.repositories.child_repository import ChildRepository
from data_storages.db.repositories.parent_repository import ParentRepository
from services.api.alfa.customer import CustomerDataService
from utils.logger import Logger
from utils.string_utils import StringUtil


class AuthenticationService:
    @staticmethod
    def is_admin_authorized(admin_telegram_id):
        admin_in_system = AdministratorRepository.find_by_telegram_id(admin_telegram_id)
        if admin_in_system:
            return True
        return False

    @staticmethod
    def is_parent_authorized(parent_telegram_id):
        parent_in_system = ParentRepository.find_by_telegram_id(parent_telegram_id)
        if parent_in_system:
            return True
        return False

    @staticmethod
    def authorize_admin(password, admin_telegram_id, username):
        if os.getenv("ADMIN_TG_BOT_PASSWORD") in password:
            AdministratorRepository.save(admin_telegram_id, username)
            return username
        else:
            return None

    # @staticmethod
    # def register_parent(phone_number, parent_telegram_id, telegram_username):
    #     normalized_phone_number = StringUtil.remove_brackets_dashes_and_spaces(phone_number)
    #     parent_children = CustomerDataService.get_customers_by_phone_number(normalized_phone_number)
    #     if parent_children:
    #         parent_name = parent_children[0].get("parent_name")
    #         parent_id = ParentRepository.save(parent_telegram_id, parent_name, normalized_phone_number,
    #                                           telegram_username)
    #         for parent_child in parent_children:
    #             child_id = parent_child.get("child_id")
    #             child_name = parent_child.get("child_name")
    #             ChildRepository.save(parent_id, child_id, child_name)
    #         return parent_name
    #     else:
    #         return None
    @staticmethod
    def authorize_parent(phone_number, parent_telegram_id, telegram_username):
        normalized_phone_number = StringUtil.remove_brackets_dashes_and_spaces(phone_number)
        parent_children = CustomerDataService.get_customers_by_phone_number(normalized_phone_number)
        if parent_children:
            parent_name = parent_children[0].get("parent_name")
            parent_id = ParentRepository.save(parent_telegram_id, parent_name, normalized_phone_number,
                                              telegram_username)
            for parent_child in parent_children:
                child_id = parent_child.get("child_id")
                child_name = parent_child.get("child_name")
                ChildRepository.save(parent_id, child_id, child_name)
            return parent_name
        else:
            return None