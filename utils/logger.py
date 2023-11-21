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
    def bot_info(user_tg_id, full_info):
        text = f"User telegram chat id: {user_tg_id}. Info: {full_info}"
        logging.info(text)

    @staticmethod
    def bot_handled_error(user_tg_id, full_info):
        text = f"User telegram chat id: {user_tg_id}. Handled Error: {full_info}"
        logging.warning(text)

    @staticmethod
    def bot_unhandled_error(full_error_info):
        logging.error(full_error_info)

    @staticmethod
    def mailing_error(full_error_info):
        logging.error(full_error_info)


