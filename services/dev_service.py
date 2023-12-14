from db_func.core import DatabaseManager
from db_func.models import Child, AbsentChild, Parent, Administrator, LessonWithAbsentChildren
from utils.constants.files_names import FN
from utils.file_utils import FileUtil


class DevService:
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
        rec_res = FileUtil.create_deprecated_mailing_results_duplicates_and_clear_original(FN.MR_RECORDINGS)
        rep_res = FileUtil.create_deprecated_mailing_results_duplicates_and_clear_original(FN.MR_REPORTS)
        bal_res = FileUtil.create_deprecated_mailing_results_duplicates_and_clear_original(FN.MR_BALANCE)
        return rec_res and rep_res and bal_res

    @staticmethod
    def clear_mailing_results():
        file_path1 = FileUtil.get_path_to_mailing_results_file(FN.MR_RECORDINGS)
        file_path2 = FileUtil.get_path_to_mailing_results_file(FN.MR_REPORTS)
        file_path3 = FileUtil.get_path_to_mailing_results_file(FN.MR_BALANCE)
        FileUtil.clear_json(file_path1)
        FileUtil.clear_json(file_path2)
        FileUtil.clear_json(file_path3)

    @staticmethod
    def clone_and_clear_logs():
        unh_res = FileUtil.create_deprecated_log_duplicates_and_clear_original(FN.LOG_UNHANDLED_ERRORS)
        han_res = FileUtil.create_deprecated_log_duplicates_and_clear_original(FN.LOG_HANDLED_ERRORS)
        info_res = FileUtil.create_deprecated_log_duplicates_and_clear_original(FN.LOG_INFO)
        return unh_res and han_res and info_res

    @staticmethod
    def clear_logs():
        file_path1 = FileUtil.get_path_to_log_file(FN.LOG_UNHANDLED_ERRORS)
        file_path2 = FileUtil.get_path_to_log_file(FN.LOG_HANDLED_ERRORS)
        file_path3 = FileUtil.get_path_to_log_file(FN.LOG_INFO)
        FileUtil.clear_txt(file_path1)
        FileUtil.clear_txt(file_path2)
        FileUtil.clear_txt(file_path3)