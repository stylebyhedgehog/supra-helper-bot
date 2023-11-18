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
    def bot_error(full_error_info):
        logging.error(full_error_info)