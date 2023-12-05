from db_func.repositories.child_repository import ChildRepository
from db_func.repositories.parent_repository import ParentRepository
from services.api.alfa.customer import CustomerDataService
from utils.logger import Logger
from utils.string_utils import StringUtil


class ParticipationService:
    @staticmethod
    def create_and_attach_to_parent_new_child(child_id, group_id):
        # todo не записывается в json
        child = ChildRepository.find_by_alfa_id(child_id)
        if child is None:
            res = CustomerDataService.get_customer_name_and_phone_numbers_by_customer_id(child_id)
            if res:
                child_name, phone_numbers = res
                normalized_phone_numbers = ParticipationService._normalize_phone_numbers(phone_numbers)
                parent = ParticipationService._find_parent_with_phone_number_in_list(normalized_phone_numbers)
                if parent:
                    ChildRepository.save(parent.id, child_id, child_name)
                    Logger.participation_info(child_id, parent.id, group_id)

            else:
                Logger.participation_handled_error(child_id, group_id)


    @staticmethod
    def _find_parent_with_phone_number_in_list(normalized_phone_numbers):
        parents = ParentRepository.find_all()
        for parent in parents:
            if parent.phone_number in normalized_phone_numbers:
                return parent
        return None


    @staticmethod
    def _normalize_phone_numbers(phone_numbers):
        res = []
        for ph_num in phone_numbers:
            norm_ph_num = StringUtil.remove_brackets_dashes_and_spaces(ph_num)
            res.append(norm_ph_num)
        return res





