import json
import os


class FileUtil:
    @staticmethod
    def get_path_to_db():
        current_directory = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_directory, "../db/sqlite.db")


    @staticmethod
    def get_path_to_tmp_json_file(filename):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_directory, f"../db/tmp_json/{filename}")

    @staticmethod
    def add_to_json_file(new_dict, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as json_file:
                old_list = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            old_list = []

        old_list.append(new_dict)

        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(old_list, json_file, indent=2, ensure_ascii=False)


    @staticmethod
    def read_from_json_file(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data_list = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            data_list = []

        return data_list