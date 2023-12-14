import logging

from utils.constants.files_names import FN
from utils.date_utils import DateUtil
from utils.file_utils import FileUtil


class Logger:

    # region API RELATED
    @staticmethod
    def api_handled_error(url, payload, params, message):
        text = f"Api \n\tUrl: {url}\n\tpayload: {payload}\n\tparams: {params}\n\tmessage: {message}"
        logging.warning(text)

        Logger._write_log_in_file(text, FN.LOG_HANDLED_ERRORS)

    @staticmethod
    def entity_not_found_error(name, **kwargs):
        text = f"Entity nor found = {name} not found\nSearch parameters"
        for key, value in kwargs.items():
            text += f"\n\t{key} = {value}"
        logging.warning(text)

        Logger._write_log_in_file(text, FN.LOG_HANDLED_ERRORS)
    # endregion
    # region BOT
    @staticmethod
    def bot_info(user_tg_id, location, full_info):
        text = f"Bot Info. Location: {location}. User telegram chat id: {user_tg_id}. Info: {full_info}"
        logging.info(text)

        Logger._write_log_in_file(text, FN.LOG_INFO)

    @staticmethod
    def bot_handled_error(user_tg_id, location, full_info):
        text = f"Bot Handled Error. Location: {location}. User telegram chat id: {user_tg_id}. Error text: {full_info}"
        logging.warning(text)

        Logger._write_log_in_file(text, FN.LOG_HANDLED_ERRORS)

    @staticmethod
    def bot_unhandled_error(user_tg_id, location, error_text, traceback_text):
        text = f"Bot Unhandled(Critical) Error. Location: {location}"
        text += f"\nUser telegram chat id: {user_tg_id}"
        text += f"\nError: {error_text}"
        text += f"\nTraceback: {traceback_text}"
        logging.error(text)

        Logger._write_log_in_file(text, FN.LOG_UNHANDLED_ERRORS)
    # endregion

    # region EXTERNAL SERVICES WEBHOOK CALL
    @staticmethod
    def webhook_call_info(external_api_name, location, call_reason, full_info):
        text = f"Webhook call. External api name: {external_api_name}. Location: {location}. Call Reason: {call_reason}. Info: {full_info}"
        logging.info(text)

        Logger._write_log_in_file(text, FN.LOG_INFO)
    # endregion
    # region MAILING
    @staticmethod
    def mailing_info(user_tg_id, location, full_info):
        text = f"Webhook Mailing Info. Location: {location}. User telegram chat id: {user_tg_id}. Info: {full_info}"
        logging.info(text)

        Logger._write_log_in_file(text, FN.LOG_INFO)

    @staticmethod
    def mailing_handled_error(location, full_info):
        text = f"Webhook Mailing Handled Error. Location: {location}. Error text: {full_info}"
        logging.warning(text)

        Logger._write_log_in_file(text, FN.LOG_HANDLED_ERRORS)

    @staticmethod
    def mailing_unhandled_error(location, error_text, traceback_text, input_data):
        text = f"Webhook Mailing Unhandled(Critical) Error. Location: {location}"
        text += f"\nError: {error_text}"
        text += f"\nInput (lesson/zoom json): {input_data}"
        text += f"\nTraceback: {traceback_text}"
        logging.error(text)

        Logger._write_log_in_file(text, FN.LOG_UNHANDLED_ERRORS)
    # endregion
    # region FLASK CONTROLLER
    @staticmethod
    def flask_controller_unhandled_error(location, error_text, traceback_text):
        text = f"Flask Controller Unhandled(Critical) Error. Location: {location}"
        text += f"\nError: {error_text}"
        text += f"\nTraceback: {traceback_text}"
        logging.error(text)

        Logger._write_log_in_file(text, FN.LOG_UNHANDLED_ERRORS)
    # endregion

   # region TEMPORARY todo: remove on fix
    @staticmethod
    def recording_completed_process(step, message):
        Logger._write_log_in_file(f"Step: {step}\nMessage: {message}", FN.LOG_INFO_RECORDINGS_COMPLETE)

    # endregion

# region PARTICIPATION
    @staticmethod
    def participation_info(child_id, parent_db_id, group_id):
        text = f"Webhook Participation Info. Location: alfa_webhook_participation. Child with child_alfa_id: {child_id} " \
               f"joined group with group_alfa_id: {group_id}. Child registered in system and attached to parent with db_id: {parent_db_id}"
        logging.info(text)

        Logger._write_log_in_file(text, FN.LOG_INFO)

    @staticmethod
    def participation_handled_error(child_id, group_id):
        text = f"Webhook Participation Handled Error. Location: alfa_webhook_participation. Child with child_alfa_id: {child_id} " \
               f"joined group with group_alfa_id: {group_id}. Due to some reasons child not found in alfa"
        logging.warning(text)

        Logger._write_log_in_file(text, FN.LOG_HANDLED_ERRORS)
# endregion

    @staticmethod
    def _write_log_in_file(text, filename):
        try:
            res = f"{10*'-'}{DateUtil.get_current_moscow_datetime_as_str()}{10 * '-'}"
            res += f"\n{text}"
            res += f"\n{30*'-'}\n"
            file_path = FileUtil.get_path_to_log_file(filename)
            FileUtil.add_to_txt_file(res, file_path)
        except Exception as e:
            logging.error(f"Error on attempt to write in file: {e}")
