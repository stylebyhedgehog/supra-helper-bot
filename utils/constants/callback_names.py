class CPP_MENU:
    BALANCE = "Баланс"  # Узнать баланс
    PERFORMANCE = "Успеваемость"  # Узнать успеваемость  ребенка
    ATTENDANCE = "Посещаемость"  # Узнать посещаемость  ребенка
    CONTACT = "Кнопка связи"  # Связаться с администратором
    MENU = [
        [BALANCE, PERFORMANCE],
        [ATTENDANCE, CONTACT]
    ]

class CPP_BALANCE:
    BASE = "par_get_bal"
    S_C = f"{BASE}_sel_child"  # Выбор ребенка

class CPP_PERFORMANCE:
    BASE = "par_get_per"
    S_C = f"{BASE}_sel_child"  # Выбор ребенка
    S_G = f"{BASE}_sel_group"  # Выбор группы
    S_M = f"{BASE}_sel_month"  # Выбор месяца

class CPP_ATTENDANCE:
    BASE = "par_get_att"
    S_C = f"{BASE}_sel_child"  # Выбор ребенка
    S_G = f"{BASE}_sel_group"  # Выбор группы
    S_M = f"{BASE}_sel_month"  # Выбор месяца


class CAP:
    AUTH_PARENT_LIST = "adm_show_authed_parents"

    menu = [
        {'text': 'Просмотр авторизованных в системе родителей', 'callback_data': AUTH_PARENT_LIST}
    ]
