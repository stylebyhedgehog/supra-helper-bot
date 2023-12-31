import os
import json
import threading

class FileUtil:
    _lock = threading.Lock()

    # GET PATH
    @staticmethod
    def get_path_to_db():
        current_directory = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_directory, "../data_storages/db/sqlite.db")

    @staticmethod
    def get_path_to_mailing_results_file(filename):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_directory, f"../data_storages/files/mailing_results/{filename}")

    @staticmethod
    def get_path_to_log_file(filename):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_directory, f"../data_storages/files/logs/{filename}")

    @staticmethod
    def create_log_and_mailing_results_files():
        # Define file paths
        log_files = ["handled_errors.txt", "unhandled_errors.txt", "info.txt"]
        mailing_files = ["balance.json", "recordings.json", "reports.json"]

        # Create log files if not exists
        for log_file in log_files:
            log_path = FileUtil.get_path_to_log_file(log_file)
            if not os.path.exists(log_path):
                with open(log_path, 'w') as file:
                    file.write("")

        # Create mailing result files if not exists
        for mailing_file in mailing_files:
            mailing_path = FileUtil.get_path_to_mailing_results_file(mailing_file)
            if not os.path.exists(mailing_path):
                if mailing_file.endswith('.json'):
                    with open(mailing_path, 'w') as file:
                        json.dump({}, file)
                else:
                    with open(mailing_path, 'w') as file:
                        file.write("")
    # JSON FILES
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
    def clear_json(file_path):
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump('', json_file, indent=2, ensure_ascii=False)

    # TXT FILES
    @staticmethod
    def add_to_txt_file(data, file_path):
        with open(file_path, 'a', encoding='utf-8') as file_to_write:
            file_to_write.write(data + '\n')

    @staticmethod
    def clear_txt(file_path):
        with open(file_path, 'w', encoding='utf-8') as file_to_write:
            file_to_write.write('')

    @staticmethod
    def read_from_txt_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file_to_read:
            content = file_to_read.read()
        return content


