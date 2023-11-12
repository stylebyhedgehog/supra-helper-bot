import os
from typing import Generator, Any

import requests
import logging


class AlfaApiTemplate:
    _TOKEN = ""

    @staticmethod
    def _authenticate() -> str:
        """
        Аутентификация пользователя и получение токена.
        """
        auth_url = "https://supra.s20.online/v2api/auth/login"
        auth_data = {"email": os.getenv("ALFA_AUTH_EMAIL"), "api_key": os.getenv("ALFA_AUTH_KEY")}

        try:
            response = requests.post(auth_url, json=auth_data)
            response.raise_for_status()
            return response.json()["token"]
        except requests.exceptions.RequestException as e:
            logging.error(f"Authentication failed: {e}")
            return ""

    @staticmethod
    def _make_authenticated_request(url: str, json_data: dict, params: dict, token: str = None) -> dict:
        """
        Отправка аутентифицированного запроса к внешнему API.
        """
        print("authed_request")
        headers = {"X-ALFACRM-TOKEN": token or AlfaApiTemplate._TOKEN}

        try:
            response = requests.post(url, headers=headers, json=json_data, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                logging.info("Token expired. Re-authenticating...")
                new_token = AlfaApiTemplate._authenticate()
                if new_token:
                    AlfaApiTemplate._TOKEN = new_token
                    return AlfaApiTemplate._make_authenticated_request(token=new_token, url=url, json_data=json_data,
                                                                       params=params)
                else:
                    logging.error(f"Unable to re-authenticate. Exiting.")
                    return {}
            else:
                logging.error(f"Request failed: {e}")
                return {}

    @staticmethod
    def fetch_paginated_data(url: str, payload: dict = None, params: dict = None) -> Generator[dict, None, None]:
        """
        Получение данных из внешнего API с поддержкой пагинации.
        """
        current_count = 0
        page = 0

        while True:
            if payload:
                payload["page"] = page
            else:
                payload = {"page": page}

            response_data = AlfaApiTemplate._make_authenticated_request(url=url, json_data=payload,
                                                                        params=params)
            if not response_data:
                logging.error(f"Request failed. Error for unspecified reasons ")
                return

            yield response_data.get("items", [])

            current_count += response_data.get("count", 0)
            if current_count >= response_data.get("total", 0):
                break

            page += 1

    @staticmethod
    def fetch_single_data(url: str, payload: dict = None, params: dict = None):
        """
        Получение единичных данных из внешнего API.
        """
        response_data = AlfaApiTemplate._make_authenticated_request(url=url, json_data=payload,
                                                                    params=params)
        if not response_data:
            logging.error(f"Request failed. Error for unspecified reasons ")
            return None

        items = response_data.get("items", [])
        if not items:
            logging.error(f"Alfa API response with empty items ")
            return None

        return items[0]
