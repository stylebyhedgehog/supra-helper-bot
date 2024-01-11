class CPP_MENU:
    BALANCE = "💴 Баланс"  # Узнать баланс
    PERFORMANCE = "🏆 Рейтинг"  # Узнать успеваемость  ребенка
    ATTENDANCE = "📊 Посещения"  # Узнать посещаемость  ребенка
    RECORDINGS = "🎥 Занятия"  # Получить запись занятия
    CONTACT = "☎ Админ"  # Связаться с администратором
    MENU = [
        [ATTENDANCE, PERFORMANCE, RECORDINGS],
        [BALANCE, CONTACT]
    ]


class CPP_ATTENDANCE:
    BASE = "par_att"
    S_C = f"{BASE}_sel_child"  # Выбор ребенка
    S_G = f"{BASE}_sel_group"  # Выбор группы
    S_M = f"{BASE}_sel_month"  # Выбор месяца


class CPP_PERFORMANCE:
    BASE = "par_per"
    S_C = f"{BASE}_sel_child"  # Выбор ребенка
    S_G = f"{BASE}_sel_group"  # Выбор группы
    S_M = f"{BASE}_sel_month"  # Выбор месяца

class CPP_RECORDINGS:
    BASE = "par_rec"
    S_C = f"{BASE}_sel_child"  # Выбор ребенка
    S_G = f"{BASE}_sel_group"  # Выбор группы
    S_L = f"{BASE}_sel_lesson"  # Выбор Занятия


class CPP_BALANCE:
    BASE = "par_bal"
    S_C = f"{BASE}_sel_child"  # Выбор ребенка

class CAP:
    AUTH_PARENT_LIST = "adm_show_authed_parents"
    NOTIFY_AUTHED_PARENTS = "adm_notify_parents"

    menu = [
        {'text': 'Просмотр авторизованных в системе родителей', 'callback_data': AUTH_PARENT_LIST},
        {'text': 'Отправить сообщение авторизованным родителям', 'callback_data': NOTIFY_AUTHED_PARENTS}
    ]
