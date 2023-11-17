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


class LessonWithAbsentChildren(Base):
    __tablename__ = 'lesson_with_absent_children'
    lesson_id = Column(Integer, primary_key=True)
    topic = Column(String)
    room_num = Column(Integer)
    start_date = Column(String)
    start_time = Column(String)
    group_id = Column(Integer)
    group_name = Column(String)


class AbsentChild(Base):
    __tablename__ = 'absent_child'
    id = Column(Integer, primary_key=True, autoincrement=True)
    child_alfa_id = Column(Integer)
    child_name = Column(String)
    lesson_with_absent_children_id = Column(Integer, ForeignKey('lesson_with_absent_children.lesson_id', ondelete='CASCADE'))
    lesson = relationship('LessonWithAbsentChildren')
