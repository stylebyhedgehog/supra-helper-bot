from data_storages.db.core import DatabaseManager
from data_storages.db.models import Child, AbsentChild, Parent, Administrator, LessonWithAbsentChildren
from utils.file_utils import FileUtil


def clear_all_tables():
    with DatabaseManager.get_db() as session:
        session.query(Child).delete()
        session.query(LessonWithAbsentChildren).delete()
        session.query(AbsentChild).delete()
        session.query(Parent).delete()
        session.query(Administrator).delete()
        session.commit()

def clear_mailing_results():
    file_path1 = FileUtil.get_path_to_mailing_results_file("recordings.json")
    file_path2 = FileUtil.get_path_to_mailing_results_file("reports.json")
    file_path3 = FileUtil.get_path_to_mailing_results_file("balance.json")
    FileUtil.clear_json(file_path1)
    FileUtil.clear_json(file_path2)
    FileUtil.clear_json(file_path3)

def clear_logs():
    file_path1 = FileUtil.get_path_to_log_file("unhandled_errors.txt")
    file_path2 = FileUtil.get_path_to_log_file("handled_errors.txt")
    file_path3 = FileUtil.get_path_to_log_file("info.txt")
    FileUtil.clear_txt(file_path1)
    FileUtil.clear_txt(file_path2)
    FileUtil.clear_txt(file_path3)