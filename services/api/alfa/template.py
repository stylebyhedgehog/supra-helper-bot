import os
import threading

import requests

from utils.logger import Logger


class AlfaApiTemplate:
    _TOKEN = ""
    _lock = threading.Lock()


    @staticmethod
    def _authenticate():
        auth_url = "https://supra.s20.online/v2api/auth/login"
        auth_data = {"email": os.getenv("ALFA_AUTH_EMAIL"), "api_key": os.getenv("ALFA_AUTH_KEY")}

        response = requests.post(auth_url, json=auth_data)
        return response.json().get("token", None)

    @staticmethod
    def _make_authenticated_request(url, json_data, params, max_retries=3):
        headers = {"X-ALFACRM-TOKEN": AlfaApiTemplate._TOKEN}

        response = requests.post(url, headers=headers, json=json_data, params=params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            if max_retries > 0:
                AlfaApiTemplate._TOKEN = AlfaApiTemplate._authenticate()
                return AlfaApiTemplate._make_authenticated_request(url=url, json_data=json_data,
                                                                   params=params, max_retries=max_retries - 1)
            else:
                Logger.api_error(url=url, payload=None, params=params, message="Unable to authenticate after 3 retries")
                return None
        else:
            Logger.api_error(url=url, payload=None, params=params, message="Unacceptable Error")
            return None

    @staticmethod
    def fetch_paginated_data(url, payload = None, params = None):
        with AlfaApiTemplate._lock:
            current_count = 0
            page = 0

            while True:
                if payload:
                    payload["page"] = page
                else:
                    payload = {"page": page}

                response_data = AlfaApiTemplate._make_authenticated_request(url=url, json_data=payload, params=params)
                if not response_data or len(response_data.get("items")) == 0:
                    Logger.api_error(url=url, payload=payload, params=params, message="Api responded with empty body")
                    return None
                yield from response_data.get("items", [])

                current_count += response_data.get("count", 0)
                if current_count >= response_data.get("total", 0):
                    break

                page += 1

    @staticmethod
    def fetch_single_data(url, payload= None, params = None):
        with AlfaApiTemplate._lock:
            response_data = AlfaApiTemplate._make_authenticated_request(url=url, json_data=payload, params=params)

            if not response_data or len(response_data.get("items", [])) == 0:
                Logger.api_error(url=url, payload=payload, params=params, message="Api responded with empty body")
                return None

            items = response_data.get("items", [])
            return items[0]
