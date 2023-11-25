import logging

from utils.date_utils import DateUtil
from utils.file_utils import FileUtil


class Logger:
    @staticmethod
    def api_handled_error(url, payload, params, message):
        text = f"Api \n\tUrl: {url}\n\tpayload: {payload}\n\tparams: {params}\n\tmessage: {message}"
        logging.warning(text)

        Logger._write_log_in_file(text, "handled_errors.txt")

    @staticmethod
    def entity_not_found_error(name, **kwargs):
        text = f"Entity nor found = {name} not found\nSearch parameters"
        for key, value in kwargs.items():
            text += f"\n\t{key} = {value}"
        logging.warning(text)

        Logger._write_log_in_file(text, "handled_errors.txt")

    # BOT
    @staticmethod
    def bot_info(user_tg_id, location, full_info):
        text = f"Bot. Location: {location}. User telegram chat id: {user_tg_id}. Info: {full_info}"
        logging.info(text)

        Logger._write_log_in_file(text, "info.txt")

    @staticmethod
    def bot_handled_error(user_tg_id, location, full_info):
        text = f"Bot Handled Error. Location: {location}. User telegram chat id: {user_tg_id}. Error text: {full_info}"
        logging.warning(text)

        Logger._write_log_in_file(text, "handled_errors.txt")

    @staticmethod
    def bot_unhandled_error(user_tg_id, location, error_text, traceback_text):
        text = f"Bot Unhandled(Critical) Error. Location: {location}"
        text += f"\nUser telegram chat id: {user_tg_id}"
        text += f"\nError: {error_text}"
        text += f"\nTraceback: {traceback_text}"
        logging.error(text)

        Logger._write_log_in_file(text, "unhandled_errors.txt")

    # EXTERNAL SERVICES WEBHOOK CALL
    @staticmethod
    def webhook_call_info(external_api_name, location, call_reason, full_info):
        text = f"Webhook call. External api name: {external_api_name}. Location: {location}. Call Reason: {call_reason}. Info: {full_info}"
        logging.info(text)

        Logger._write_log_in_file(text, "info.txt")

    # MAILING
    @staticmethod
    def mailing_info(user_tg_id, location, full_info):
        text = f"Mailing. Location: {location}. User telegram chat id: {user_tg_id}. Info: {full_info}"
        logging.info(text)

        Logger._write_log_in_file(text, "info.txt")

    @staticmethod
    def mailing_handled_error(location, full_info):
        text = f"Mailing Handled Error. Location: {location}. Error text: {full_info}"
        logging.warning(text)

        Logger._write_log_in_file(text, "handled_errors.txt")

    @staticmethod
    def mailing_unhandled_error(location, error_text, traceback_text, input_data):
        text = f"Mailing Unhandled(Critical) Error. Location: {location}"
        text += f"\nError: {error_text}"
        text += f"\nInput (lesson/zoom json): {input_data}"
        text += f"\nTraceback: {traceback_text}"
        logging.error(text)

        Logger._write_log_in_file(text, "unhandled_errors.txt")

    # FLASK CONTROLLER
    @staticmethod
    def flask_controller_unhandled_error(location, error_text, traceback_text):
        text = f"Flask Controller Unhandled(Critical) Error. Location: {location}"
        text += f"\nError: {error_text}"
        text += f"\nTraceback: {traceback_text}"
        logging.error(text)

        Logger._write_log_in_file(text, "unhandled_errors.txt")

    @staticmethod
    def _write_log_in_file(text, filename):
        res = f"{10*'-'}{DateUtil.get_current_moscow_time_as_str()}{10 * '-'}"
        res += f"\n{text}"
        res += f"\n{30*'-'}\n"
        file_path = FileUtil.get_path_to_log_file(filename)
        FileUtil.add_to_txt_file(res, file_path)

