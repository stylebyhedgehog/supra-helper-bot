class CPP:
    MENU_BALANCE = "Баланс"  # Узнать баланс
    BALANCE = "par_get_bal"
    BALANCE_S_C = f"{BALANCE}_select_child"  # Выбор ребенка

    MENU_PERFORMANCE = "Успеваемость"  # Узнать успеваемость  ребенка
    PERFORMANCE = "par_get_per"
    PERFORMANCE_S_C = f"{PERFORMANCE}_select_child"  # Выбор ребенка
    PERFORMANCE_S_G = f"{PERFORMANCE}_select_group"  # Выбор группы
    PERFORMANCE_S_M = f"{PERFORMANCE}_select_month"  # Выбор месяца

    MENU_ATTENDANCE = "Посещаемость"  # Узнать посещаемость  ребенка
    ATTENDANCE = "par_get_att"
    ATTENDANCE_S_C = f"{ATTENDANCE}_select_child"  # Выбор ребенка
    ATTENDANCE_S_G = f"{ATTENDANCE}_select_group"  # Выбор группы
    ATTENDANCE_S_M = f"{ATTENDANCE}_select_month"  # Выбор месяца

    MENU_CONTACT = "Кнопка связи"  # Связаться с администратором
    menu = [
        [MENU_BALANCE, MENU_PERFORMANCE],
        [MENU_ATTENDANCE, MENU_CONTACT]
    ]


class CAP:
    AUTH_PARENT_LIST = "adm_show_authed_parents"

    menu = [
        {'text': 'Просмотр авторизованных в системе родителей', 'callback_data': AUTH_PARENT_LIST}
    ]
