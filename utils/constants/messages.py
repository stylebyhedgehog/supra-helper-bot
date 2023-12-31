class PAM_MENU:
    INFO_PRE_AUTH = "Используйте команду /login_admin password для прохождения авторизации. (Вместо password введите пароль)"

class PPM_MENU:
    INFO_PRE_AUTH = "Используйте команду /login для прохождения авторизации."
    INFO_POST_AUTH = "Меню c доступными функциями отображено под клавиатурой"


# Сообщения бота при выполнении администратором активности "Авторизация в системе"
class PAM_AUTH:
    # Ошибка в случае попытки администратора повторно зарегистрироваться в системе с того же аккаунта
    ERROR_ALREADY_AUTHENTICATED = "Вы уже авторизованы в системе\nИспользуйте команду /help для просмотра доступных функций."

    # Ошибка в случае ввода администратором неверного пароля
    ERROR_WRONG_PASSWORD = "Неверный пароль администратора"

    # Результат в положительном случае потока события
    RESULT = lambda username: f"Вы успешно авторизованы как администратор. Зарегистрированное имя {username}"


# Сообщения бота при выполнении родителем активности "Авторизация в системе"
class PPM_AUTH:
    # Ошибка в случае попытки родителя повторно зарегистрироваться в системе с того же аккаунта
    ERROR_ALREADY_AUTHENTICATED = "Вы уже авторизованы в системе\nИспользуйте команду /help для просмотра доступных функций."

    ERROR_PHONE_NUMBER_ALREADY_USED = "Невозможно реализовать авторизацию. Пользователь с таким номером телефона уже авторизован."

    # Ошибка в одном из следующих случаев:
    # 1. В alfa.crm отсутствуют дети, у которых указан номер телефона, введенный родителем
    # 2. Родитель ввел некорректный номер телефона
    ERROR_AUTH_FAILED = "Невозможно осуществить авторизацию"

    # Информационное сообщение, появляющееся при использовании родителем команды /login
    INFO_AUTH_METHOD_SELECTION = "Выберите способ авторизации: "

    # Способы авторизации в виде кнопок (появляются после команды /login)
    BUTTON_AUTH_METHOD_MANUAL_INPUT = "Ввести номер телефона вручную"
    BUTTON_AUTH_METHOD_TG_FETCH = "Использовать номер из аккаунта telegram"

    # Информационное сообщение, появляющееся после выбора родителем ручного способа ввода номера телефона
    INFO_AUTH_METHOD_MANUAL_INPUT_HINT = "Введите номер телефона в формате +XXXXXXX\nПример: +79531302250:"

    # Информационное сообщение, появляющееся после выбора родителем способа авторизации на основе номера в телеграм
    INFO_AUTH_METHOD_TG_FETCH_HINT = "Нажмите на кнопку 'Отправить номер', чтобы отправить свой номер телефона:"

    # Кнопка для отправки номера телефона, привязанного к аккаунту тг
    BUTTON_AUTH_METHOD_TG_FETCH_PROCESS = "Отправить номер"

    # Результат в положительном случае потока события
    RESULT = lambda children_list: \
        f"""
Вы успешно прошли процесс авторизации!
Теперь вы можете отслеживать информацию о следующих учениках:
{children_list}

Используйте команду /help, чтобы получить доступные функции
        """


# Сообщения бота при выполнении активности "Узнать баланс"
class PPM_BALANCE:
    # Необработанная ошибка
    ERROR_UNHANDLED = "Ошибка системы! Не удалось получить информацию о балансе."

    # Ошибка в случае отсутсвия в системе детей, привязанных к родителю
    ERROR_CHILDREN_NOT_FOUND = "Ошибка системы! Не удалось получить информацию об учениках."

    # Информационное сообщение, к которому прикрепляются кнопки с именами детей (если у родителя >1 ребенка)
    INFO_CHILD_SELECTION = "Выберите ребенка, у которого хотите проверить баланс:"

    # Результат в положительном случае потока события
    RESULT = lambda child_name, balance, paid_count: f"{child_name}: Текущий баланс: {balance}, осталось {paid_count} уроков"


class PPM_CONTACT:
    # Ошибка в случае отсутсвия в системе зарегистрированных администраторов
    ERROR_ADMIN_NOT_FOUND = "Ошибка системы! Не удалось получить контакты доступных администраторов."

    # Результат в положительном случае потока события
    RESULT = lambda admin_username: f"Аккаунт администратора: @{admin_username}"


class PPM_STUDY_RESULTS:
    ERROR_CHILDREN_NOT_FOUND = "Ошибка системы! Не удалось получить информацию об учениках."
    ERROR_GROUPS_NOT_FOUND = "Ошибка системы! Не удалось получить информацию о группах."
    ERROR_MONTHS_NOT_FOUND = "Ошибка системы! Не удалось получить информацию о занятиях."
    ERROR_LESSONS_NOT_FOUND = "Ошибка системы! Не удалось получить информацию о занятиях за выбранный Вами период."
    INFO_CHILD_SELECTION = "Выберите ребенка:"
    INFO_GROUP_SELECTION = "Выберите группу:"
    INFO_MONTH_SELECTION = "Выберите месяц:"
    INFO_NOT_AVAILABLE = None
    RESULT = None

class PPM_ATTENDANCE(PPM_STUDY_RESULTS):
    RESULT = lambda lessons_amount, attended_lessons_amount, average_attendance: \
        f"""
За выбранный Вами период было проведено {lessons_amount} занятий.

Посещаемость - {average_attendance}% ({attended_lessons_amount}/{lessons_amount})
        """


class PPM_PERFORMANCE(PPM_STUDY_RESULTS):
    INFO_NOT_AVAILABLE = "Функция проверки успеваемости недоступна для групп по Английскому языку"
    RESULT = lambda month_name, lessons_amount, average_performance, topic_performance:\
        f"""
За выбранный Вами период ({month_name}) у нас прошло {lessons_amount} занятий .

📖 Перечень освоенных тем:

{topic_performance} 

Средняя оценка: {average_performance}%
            """


# Сообщения бота при выполнении активности "Рассылка отчетов"
class PPM_REPORT_DISPATCHING:
    RESULT_CC = lambda month_name, lessons_amount, subject_name, attendance_rate, \
                       attendance_amount, topic_performance_rate_list, teacher_feedback: \
        f"""
Добрый день! Будем рады поделиться промежуточными результатами обучения за {month_name.lower()}.
📝 У нас прошло {lessons_amount} занятий в рамках курса {subject_name}.
📊 Посещаемость - {attendance_rate}% ({attendance_amount}/{lessons_amount})

📖 В рамках блока занятий освоены следующие темы:

{topic_performance_rate_list} 

Преподаватель отмечает, что {teacher_feedback} 

🏆 Будем благодарны за оценку нашей образовательной услуги в прошлом месяце: от 0 до 10 (где 0 - совсем не понравилось, 10 - все отлично, пожеланий нет).
Мы всегда открыты к вашим вопросам и пожеланиям по процессу обучения! 

С уважением, команда онлайн-академии Supra
        """

    RESULT_EC = lambda month_name, lessons_amount, attendance_rate, attendance_amount, teacher_feedback: \
        f"""
Добрый день! Будем рады поделиться промежуточными результатами обучения за {month_name.lower()}.
📝 У нас прошло {lessons_amount} занятий.
📊 Посещаемость - {attendance_rate}% ({attendance_amount}/{lessons_amount})

Преподаватель отмечает, что {teacher_feedback} 

🏆 Будем благодарны за оценку нашей образовательной услуги в прошлом месяце: от 0 до 10 (где 0 - совсем не понравилось, 10 - все отлично, пожеланий нет).
Мы всегда открыты к вашим вопросам и пожеланиям по процессу обучения! 

С уважением, команда онлайн-академии Supra
        """


# Сообщения бота при выполнении активности "Рассылка отчетов"
class PPM_ZOOM_RECORDINGS_DISPATCHING:
    RESULT = lambda lesson_topic, recording_url, group_name, start_date, start_time: \
        f"""
Ввиду пропуска занятия от {start_date} {start_time} в группе {group_name} отправляем Вам запись занятия.

Тема занятия: {lesson_topic}
Ссылка на запись: {recording_url}
        """


# Сообщения бота при выполнении активности "Рассылка информации о необходимости пополнить баланс"
class PPM_BALANCE_NOTIFICATION_DISPATCHING:
    RESULT = lambda balance, paid_count, child_name: \
        f"""
У {child_name} на текущий момент осталось {paid_count} занятий.
        """
