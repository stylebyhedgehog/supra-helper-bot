from datetime import timezone, timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta
en_month_ru_month = {
    "January": "Январь",
    "February": "Февраль",
    "March": "Март",
    "April": "Апрель",
    "May": "Май",
    "June": "Июнь",
    "July": "Июль",
    "August": "Август",
    "September": "Сентябрь",
    "October": "Октябрь",
    "November": "Ноябрь",
    "December": "Декабрь"
}


class DateUtil:

    @staticmethod
    def _get_current_moscow_time():
        current_time_utc = datetime.utcnow()
        moscow_time_difference = timedelta(hours=3)
        current_time_moscow = current_time_utc + moscow_time_difference
        return current_time_moscow

    @staticmethod
    def generate_month_names(start_date_str, end_date_str):
        start_date = datetime.strptime(start_date_str, "%Y-%m")
        end_date = datetime.strptime(end_date_str, "%Y-%m")

        month_list = []

        while start_date <= end_date:
            month_name = en_month_ru_month[start_date.strftime("%B")]
            year_month = start_date.strftime("%Y-%m")

            month_name += " " + start_date.strftime("%Y")

            month_dict = {
                "month_name": month_name,
                "year_month": year_month
            }

            month_list.append(month_dict)
            start_date += relativedelta(months=1)

        return month_list

    @staticmethod
    def get_month_name(date_str):
        date_object = datetime.strptime(date_str, '%Y-%m')

        month_number = date_object.month

        months = {
            1: 'Январь',
            2: 'Февраль',
            3: 'Март',
            4: 'Апрель',
            5: 'Май',
            6: 'Июнь',
            7: 'Июль',
            8: 'Август',
            9: 'Сентябрь',
            10: 'Октябрь',
            11: 'Ноябрь',
            12: 'Декабрь'
        }

        return months.get(month_number)

    @staticmethod
    def next_month(date_str):
        current_date = datetime.strptime(date_str, "%Y-%m")
        next_month_date = current_date + timedelta(days=32)
        next_month_date = next_month_date.replace(day=1)
        return next_month_date.strftime("%Y-%m")

    @staticmethod
    def get_date_week_ago_and_current():
        current_time_moscow = DateUtil._get_current_moscow_time()
        last_week_date = current_time_moscow - timedelta(weeks=1)

        last_week_date_str = last_week_date.strftime('%Y-%m-%d')
        current_date_str = current_time_moscow.strftime('%Y-%m-%d')
        return last_week_date_str, current_date_str

    @staticmethod
    def normalize_date(date_str):
        date_object = datetime.strptime(date_str, "%d.%m.%Y")
        normalized_date = date_object.strftime("%Y-%m-%d")
        return normalized_date

    @staticmethod
    def remove_day(date_str):
        y, m, d = date_str.split("-")
        return y + "-" + m

    @staticmethod
    def moscow_to_utc(moscow_date):
        moscow_datetime = datetime.strptime(moscow_date, '%Y-%m-%d %H:%M:%S')
        moscow_timezone = timezone(timedelta(hours=3))
        moscow_datetime = moscow_datetime.replace(tzinfo=moscow_timezone)
        utc_datetime = moscow_datetime.astimezone(timezone.utc)
        utc_date = utc_datetime.strftime('%Y-%m-%d')
        utc_time = utc_datetime.strftime('%H:%M')
        return utc_date, utc_time

    @staticmethod
    def utc_to_moscow(input_time_str):
        input_time = datetime.strptime(input_time_str, "%Y-%m-%dT%H:%M:%SZ")
        utc_offset = timezone(timedelta(hours=3))
        moscow_time = input_time.replace(tzinfo=timezone.utc).astimezone(utc_offset)
        result_str = moscow_time.strftime("%Y-%m-%d")
        return result_str

    @staticmethod
    def extract_date_and_time(date_time):
        moscow_datetime = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        utc_date = moscow_datetime.strftime('%Y-%m-%d')
        utc_time = moscow_datetime.strftime('%H:%M')
        return utc_date, utc_time

    @staticmethod
    def get_current_moscow_time_as_str():
        current_time_moscow = DateUtil._get_current_moscow_time()
        return current_time_moscow.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_current_moscow_date_y_m():
        current_time_utc = datetime.utcnow()
        moscow_time_difference = timedelta(hours=3)
        current_time_moscow = current_time_utc + moscow_time_difference
        return current_time_moscow.strftime('%Y-%m')
    @staticmethod
    def earlier_date(date_str1, date_str2):
        date_format = "%Y-%m"

        date1 = datetime.strptime(date_str1, date_format)
        date2 = datetime.strptime(date_str2, date_format)

        return min(date1, date2).strftime(date_format)


