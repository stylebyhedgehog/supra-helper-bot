import os

from db.repositories.administrator_repository import AdministratorRepository
from db.repositories.child_repository import ChildRepository
from db.repositories.parent_repository import ParentRepository
from services.api.alfa.customer import CustomerFetcher, CustomerDataService
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

    @staticmethod
    def authorize_parent(phone_number, parent_telegram_id):
        normalized_phone_number = StringUtil.remove_brackets_dashes_and_spaces(phone_number)
        parent_children = CustomerDataService.get_customers_by_phone_number(normalized_phone_number)
        saved_children_names = []
        if parent_children:
            parent_name = parent_children[0].get("parent_name")
            ParentRepository.save(parent_telegram_id, parent_name, normalized_phone_number)
            for parent_child in parent_children:
                child_id = parent_child.get("child_id")
                child_name = parent_child.get("child_name")
                ChildRepository.save(parent_telegram_id, child_id, child_name)
                saved_children_names.append(child_name)
            return parent_name, saved_children_names
        else:
            return None
