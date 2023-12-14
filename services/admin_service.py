from db_func.core import DatabaseManager
from db_func.models import Child, AbsentChild, Parent, Administrator, LessonWithAbsentChildren
from utils.file_utils import FileUtil


class AdminService:
    @staticmethod
    def clear_all_tables():
        with DatabaseManager.get_db() as session:
            session.query(Child).delete()
            session.query(LessonWithAbsentChildren).delete()
            session.query(AbsentChild).delete()
            session.query(Parent).delete()
            session.query(Administrator).delete()
            session.commit()

    @staticmethod
    def clone_and_clear_mailing_results():
        rec_res = FileUtil.create_deprecated_mailing_results_duplicates("recordings.json")
        rep_res = FileUtil.create_deprecated_mailing_results_duplicates("reports.json")
        bal_res = FileUtil.create_deprecated_mailing_results_duplicates("balance.json")
        return rec_res and rep_res and bal_res

    @staticmethod
    def clear_mailing_results():
        file_path1 = FileUtil.get_path_to_mailing_results_file("recordings.json")
        file_path2 = FileUtil.get_path_to_mailing_results_file("reports.json")
        file_path3 = FileUtil.get_path_to_mailing_results_file("balance.json")
        FileUtil.clear_json(file_path1)
        FileUtil.clear_json(file_path2)
        FileUtil.clear_json(file_path3)

    @staticmethod
    def clone_and_clear_logs():
        unh_res = FileUtil.create_deprecated_log_duplicates("unhandled_errors.txt")
        han_res = FileUtil.create_deprecated_log_duplicates("handled_errors.txt")
        info_res = FileUtil.create_deprecated_log_duplicates("info.txt")
        return unh_res and han_res and info_res

    @staticmethod
    def clear_logs():
        file_path1 = FileUtil.get_path_to_log_file("unhandled_errors.txt")
        file_path2 = FileUtil.get_path_to_log_file("handled_errors.txt")
        file_path3 = FileUtil.get_path_to_log_file("info.txt")
        FileUtil.clear_txt(file_path1)
        FileUtil.clear_txt(file_path2)
        FileUtil.clear_txt(file_path3)