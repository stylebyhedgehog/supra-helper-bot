import json
import os


class TestUtils:
    @staticmethod
    def is_group_lesson_conducted(data):
        if data["fields_new"]["status"] == 3 and data["fields_rel"]["lesson_type_id"] == 2:
            return True
        else:
            return False

    @staticmethod
    def append_to_file(text, filename):
        with open(TestUtils.get_path_to_test_file(filename), "a", encoding="utf-8") as file:
            file.write(text +"\n")

    @staticmethod
    def add_to_json_file(new_dict, file):
        try:
            with open(file, 'r', encoding='utf-8') as json_file:
                old_list = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            old_list = []

        old_list.append(new_dict)

        with open(file, 'w', encoding='utf-8') as json_file:
            json.dump(old_list, json_file, indent=2, ensure_ascii=False)

    @staticmethod
    def read_from_json_file(file):
        try:
            with open(file, 'r', encoding='utf-8') as json_file:
                data_list = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            data_list = []

        return data_list

    @staticmethod
    def get_path_to_test_file(filename):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_directory, f"../tests/{filename}")