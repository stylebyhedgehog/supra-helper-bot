from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Administrator(Base):
    __tablename__ = 'administrator'
    telegram_id = Column(Integer, primary_key=True)
    telegram_username = Column(String)


class Parent(Base):
    __tablename__ = 'parent'
    telegram_id = Column(Integer, primary_key=True)
    name = Column(String)
    phone_number = Column(String)


class Child(Base):
    __tablename__ = 'child'
    child_alfa_id = Column(Integer, primary_key=True, autoincrement=True)
    parent_telegram_id = Column(Integer, ForeignKey('parent.telegram_id'))
    child_name = Column(String)


class AbsentChild(Base):
    __tablename__ = 'absent_child'
    id = Column(Integer, primary_key=True)
    room_num = Column(Integer)
    start_date = Column(String)
    start_time = Column(String)
    group_alfa_id = Column(Integer)
    group_alfa_name = Column(String)
    child_alfa_id = Column(Integer)
    topic = Column(String)
