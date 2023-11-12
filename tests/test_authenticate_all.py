import os

from dotenv import load_dotenv

from services.admin_service import clear_all_tables
from services.api.alfa.customer import CustomerFetcher
from services.bot.authentication_service import AuthenticationService
from utils.string_utils import StringUtil


def authenticate_all():
    i = 0
    customers = CustomerFetcher.all()
    unique_phones = set()
    for customer in customers:
        phones = customer.get("phone")
        if len(phones) > 0:
            unique_phones.add(phones[0])
        else:
            unique_phones.add("EMPTY")

    for unique_phone in unique_phones:
        RES = AuthenticationService.authorize_parent(unique_phone, i)
        if RES:
            parent_name, saved_children_names = RES
            print(parent_name, saved_children_names)
        i+=1
