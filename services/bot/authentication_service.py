import os

from data_storages.db.repositories.administrator_repository import AdministratorRepository
from data_storages.db.repositories.child_repository import ChildRepository
from data_storages.db.repositories.parent_repository import ParentRepository
from services.api.alfa.customer import CustomerDataService
from utils.string_utils import StringUtil


class AuthenticationService:
    @staticmethod
    def is_admin_authorized(admin_telegram_id):
        admin_in_system = AdministratorRepository.find_by_telegram_id(admin_telegram_id)
        if admin_in_system:
            return True
        return False

    @staticmethod
    def is_parent_with_tg_id_authorized(parent_telegram_id):
        parent_in_system = ParentRepository.find_by_telegram_id(parent_telegram_id)
        if parent_in_system:
            return True
        return False

    @staticmethod
    def is_parent_with_phone_number_authorized(phone_number):
        normalized_phone_number = StringUtil.remove_brackets_dashes_and_spaces(phone_number)
        parent_in_system = ParentRepository.find_by_phone_number(normalized_phone_number)
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
    def authorize_parent(phone_number, parent_telegram_id, telegram_username):
        normalized_phone_number = StringUtil.remove_brackets_dashes_and_spaces(phone_number)
        parent_children = CustomerDataService.get_customers_by_phone_number(normalized_phone_number)
        saved_children_names = []
        if parent_children:
            parent_name = parent_children[0].get("parent_name")
            parent_id = ParentRepository.save(parent_telegram_id, parent_name, normalized_phone_number,
                                              telegram_username)
            for parent_child in parent_children:
                child_id = parent_child.get("child_id")
                child_name = parent_child.get("child_name")
                ChildRepository.save(parent_id, child_id, child_name)
                saved_children_names.append(child_name)
            return parent_name, saved_children_names
        else:
            return None

    @staticmethod
    def logout_parent(parent_telegram_id):
        res1 = ChildRepository.delete_by_parent_tg_id(parent_telegram_id)
        res2 = ParentRepository.delete_by_telegram_id(parent_telegram_id)
        if res1 and res2:
            return "children and parent removed"
        else:
            resp = ""
            if not res1:
                resp += "children not removed"
            if not res2:
                resp += "parents not removed"
            return  resp

