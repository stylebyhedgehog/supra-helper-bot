import re


class StringUtil:
    @staticmethod
    def remove_brackets_dashes_and_spaces(input_string):  # удаляет лишние символы в номере телефона
        result_string = input_string.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')

        return result_string

    @staticmethod
    def extract_number_in_brackets(input_string):  # извлекает id группы из []
        start_index = input_string.find('[')
        end_index = input_string.find(']')

        if start_index != -1 and end_index != -1 and start_index < end_index:
            value_in_brackets = input_string[start_index + 1:end_index]
            return int(value_in_brackets)
        else:
            return None

    @staticmethod
    def extract_number_from_email(email):
        match = re.search(r'\d+', email)

        if match:
            number = int(match.group())
            return number
        else:
            return None

    @staticmethod
    def list_to_string(lst):
        res = ""
        for el in lst:
            res += f"\n{el}"
        return res

    @staticmethod
    def is_contain_feedback(note):
        return len(note) > 0 and note.lower().startswith("ос:")

    @staticmethod
    def extract_teacher_feedback(note):
        return note[2:]

    # @staticmethod
    # def extract_normalized_subject_name(text):
    #     return text[3:]

    @staticmethod
    def extract_course_subject(full_name):
        course_name, subject_name = full_name.split(":")
        return StringUtil.remove_spaces(course_name), StringUtil.remove_spaces(subject_name)


    @staticmethod
    def remove_spaces(string):
        return string.replace(" ", "")