import os


def get_path_to_db():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_directory, "../db/sqlite.db")

