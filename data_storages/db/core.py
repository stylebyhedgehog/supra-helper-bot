from sqlalchemy import create_engine, inspect, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from data_storages.db.models import Base


class DatabaseManager:
    _db_instance = None
    session = None

    def __init__(self, db_uri):
        engine = create_engine(db_uri)
        self.Session = scoped_session(sessionmaker(bind=engine))

    @classmethod
    def init_db(cls, db_uri):
        if not cls._db_instance:
            cls._db_instance = cls(db_uri)
            cls.create_tables()
    @classmethod
    def create_tables(cls):
        if not cls._db_instance:
            raise Exception("Database not initialized. Call init_db() first.")
        Base.metadata.create_all(cls._db_instance.Session().get_bind())

    @classmethod
    def get_db(cls):
        if not cls._db_instance:
            raise Exception("Database not initialized. Call init_db() first.")
        return cls._db_instance.Session()

    @classmethod
    def get_all_records(cls):
        if not cls._db_instance:
            raise Exception("Database not initialized. Call init_db() first.")

        session = cls._db_instance.Session()
        result = {}

        metadata = MetaData()
        metadata.reflect(bind=session.get_bind())

        for table in metadata.tables.values():
            records = session.query(table).all()
            result[table.name] = records

        return result
