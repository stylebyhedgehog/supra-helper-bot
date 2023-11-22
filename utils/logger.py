import logging


class Logger:
    @staticmethod
    def api_error(url, payload, params, message):
        logging.error(f"Api Error\n\tUrl: {url}\n\tpayload: {payload}\n\tparams: {params}\n\tmessage: {message}")


    @staticmethod
    def entity_not_found_error(name, **kwargs):
        text = f"Entity with name = {name} not found\nSearch parameters"
        for key, value in kwargs.items():
            text += f"\n\t{key} = {value}"
        logging.error(text)

    @staticmethod
    def bot_info(user_tg_id, location, full_info):
        text = f"Bot. Location: {location}. User telegram chat id: {user_tg_id}. Info: {full_info}"
        logging.info(text)

    @staticmethod
    def bot_handled_error(user_tg_id, location, full_info):
        text = f"Bot Handled Error. Location: {location}. User telegram chat id: {user_tg_id}. Error text: {full_info}"
        logging.warning(text)

    @staticmethod
    def bot_unhandled_error(user_tg_id, location, error_text, traceback_text):
        text = f"Bot Unhandled(Critical) Error. Location: {location}"
        text += f"\nUser telegram chat id: {user_tg_id}"
        text += f"\nError: {error_text}"
        text += f"\nTraceback: {traceback_text}"
        logging.error(text)

    @staticmethod
    def mailing_info(user_tg_id, location, full_info):
        text = f"Mailing. Location: {location}. User telegram chat id: {user_tg_id}. Info: {full_info}"
        logging.info(text)

    @staticmethod
    def mailing_handled_error(location, full_info):
        text = f"Bot Handled Error. Location: {location}. Error text: {full_info}"
        logging.warning(text)


    @staticmethod
    def mailing_unhandled_error(location, error_text, traceback_text, input_data):
        text = f"Mailing Unhandled(Critical) Error. Location: {location}"
        text += f"\nError: {error_text}"
        text += f"\nInput (lesson/zoom json): {input_data}"
        text += f"\nTraceback: {traceback_text}"
        logging.error(text)


