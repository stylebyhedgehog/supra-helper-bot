import logging
import os
import json
import shutil
import threading

from utils.constants.files_names import FN


class FileUtil:
    _lock = threading.Lock()

    # region GET PATH
    @staticmethod
    def get_path_to_db():
        if os.getenv("HOSTING") == "AMVERA":
            return "/data/sqlite.db"
        current_directory = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_directory, "../data/db/sqlite.db")

    @staticmethod
    def get_path_to_mailing_results_file(filename):
        if os.getenv("HOSTING") == "AMVERA":
            return f"/data/{filename}"
        current_directory = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_directory, f"../data/mailing_results/{filename}")

    @staticmethod
    def get_path_to_log_file(filename):
        if os.getenv("HOSTING") == "AMVERA":
            return f"/data/{filename}"
        current_directory = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_directory, f"../data/logs/{filename}")

    # endregion
    @staticmethod
    def create_log_and_mailing_results_files():
        log_files = FN.LIST_LOG_FILES
        mailing_files = FN.LIST_MAILING_RESULTS_FILES

        for log_file in log_files:
            log_path = FileUtil.get_path_to_log_file(log_file)
            if not os.path.exists(log_path):
                with open(log_path, 'w') as file:
                    file.write("")

        for mailing_file in mailing_files:
            mailing_path = FileUtil.get_path_to_mailing_results_file(mailing_file)
            if not os.path.exists(mailing_path):
                if mailing_file.endswith('.json'):
                    with open(mailing_path, 'w') as file:
                        json.dump({}, file)
                else:
                    with open(mailing_path, 'w') as file:
                        file.write("")

    # region JSON FILES
    @staticmethod
    def add_to_json_file(new_dict, file_path):
        with FileUtil._lock:
            try:
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    old_list = json.load(json_file)
            except (FileNotFoundError, json.JSONDecodeError):
                old_list = []
            if len(old_list) == 0:
                old_list = []
            old_list.append(new_dict)

            with open(file_path, 'w', encoding='utf-8') as json_file:
                json.dump(old_list, json_file, indent=2, ensure_ascii=False)

    @staticmethod
    def read_from_json_file(file_path):
        with FileUtil._lock:
            try:
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    data_list = json.load(json_file)
            except (FileNotFoundError, json.JSONDecodeError):
                data_list = []

        return data_list

    @staticmethod
    def create_deprecated_mailing_results_duplicates_and_clear_original(filename):
        try:
            original_path = FileUtil.get_path_to_mailing_results_file(filename)
            deprecated_filename = f"{filename.split('.')[0]}_deprecated.{filename.split('.')[1]}"
            deprecated_path = FileUtil.get_path_to_mailing_results_file(deprecated_filename)
            shutil.copy(original_path, deprecated_path)

            with open(original_path, 'w') as original_file:
                original_file.truncate()

            return True
        except Exception as e:
            logging.error(f"Error on creating mailing results duplicate: {e}")
            return False

    @staticmethod
    def clear_json(file_path):
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump('', json_file, indent=2, ensure_ascii=False)

    # endregion

    # TXT FILES
    @staticmethod
    def add_to_txt_file(data, file_path):
        with open(file_path, 'a', encoding='utf-8') as file_to_write:
            file_to_write.write(data + '\n')

    @staticmethod
    def read_from_txt_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file_to_read:
            content = file_to_read.read()
        return content

    @staticmethod
    def create_deprecated_log_duplicates_and_clear_original(filename):
        try:
            original_path = FileUtil.get_path_to_log_file(filename)
            deprecated_filename = f"{filename.split('.')[0]}_deprecated.{filename.split('.')[1]}"
            deprecated_path = FileUtil.get_path_to_log_file(deprecated_filename)
            shutil.copy(original_path, deprecated_path)

            with open(original_path, 'w') as original_file:
                original_file.truncate()

            return True
        except Exception as e:
            logging.error(f"Error on creating logs duplicate: {e}")
            return False

    @staticmethod
    def clear_txt(file_path):
        with open(file_path, 'w', encoding='utf-8') as file_to_write:
            file_to_write.write('')

    # endregion

    @staticmethod
    def get_data_size():
        if os.getenv("HOSTING") == "AMVERA":
            folder_path = "/data"

            total_size = 0
            for dirpath, dirnames, filenames in os.walk(folder_path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(filepath)
            size_in_mb = total_size / 1024 / 1024

            return f"Размер данных: {size_in_mb:.2f} МБ"
        else:
            return "Недоступно для хостингов кроме Amvera"
