import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import scoped_session, sessionmaker

class DatabaseManager:
    _db_instance = None

    def __init__(self, db_uri):
        engine = create_engine(db_uri)
        Session = sessionmaker(bind=engine)
        self.session = scoped_session(Session)

    @classmethod
    def init_db(cls, db_uri):
        if not cls._db_instance:
            cls._db_instance = cls(db_uri)

    @classmethod
    def get_db(cls):
        if not cls._db_instance:
            raise Exception("Database not initialized. Call init_db() first.")
        return cls._db_instance.session()


# class DatabaseManager:
#     _db_instance = None
#
#     def __init__(self, db_uri):
#         engine = create_engine(db_uri)
#         Session = sessionmaker(bind=engine)
#         self.session = Session()
#
#     @classmethod
#     def init_db(cls, db_uri):
#         if not cls._db_instance:
#             cls._db_instance = cls(db_uri)
#
#     @classmethod
#     def get_db(cls):
#         if not cls._db_instance:
#             raise Exception("Database not initialized. Call init_db() first.")
#         return cls._db_instance.session


