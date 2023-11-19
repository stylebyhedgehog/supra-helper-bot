import threading
from services.api.alfa.customer import CustomerFetcher
from services.bot.authentication_service import AuthenticationService


def test_authenticate_all_in_one_thread():
    customers = CustomerFetcher.all()
    unique_phones = set()
    for customer in customers:
        phones = customer.get("phone")
        if len(phones) > 0:
            unique_phones.add(phones[0])
        else:
            unique_phones.add("EMPTY")

    i = 0
    for unique_phone in unique_phones:
        res = AuthenticationService.authorize_parent(unique_phone, i, "u_name")
        i+=1
        print(res)
def threadable_task(unique_phone, i):
    res = AuthenticationService.authorize_parent(unique_phone, i, "u_name")
    print(res)

def test_authenticate_all_in_multy_threads():
    customers = CustomerFetcher.all()
    unique_phones = set()
    for customer in customers:
        phones = customer.get("phone")
        if len(phones) > 0:
            unique_phones.add(phones[0])
        else:
            unique_phones.add("EMPTY")

    threads = []
    i = 0

    for unique_phone in unique_phones:
        i+=1
        thread = threading.Thread(target=threadable_task, args=(unique_phone,i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
