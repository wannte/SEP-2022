from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    student_id = Column(String(8), unique=True, nullable=False)
    major = Column(String(20), nullable=False)

class Lecture(Base):
    __tablename__ = "lectures"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    lecture_code = Column(String(6), nullable=False)
    lecture_name = Column(String(40), nullable=False)
    year = Column(String(4), nullable=False)
    semester = Column(String(10), nullable=False)
    required = Column(Boolean, default=False, nullable=False)
    major = Column(String(20), nullable=False)
    credit = Column(Integer, nullable=False, default=3)

# class CustomLecture(Base):
#     __tablename__ = "custom_lectures"

#     id = Column(Integer, primary_key=True, index=True, nullable=False)
#     name = Column(String(40), nullable=False)
#     year = Column(Integer, nullable=False)
#     semester = Column(String(3), nullable=False)
#     major = Column(String(20), nullable=False)
#     credit = Column(Integer, nullable=False, default=3)

class Learned(Base):
    __tablename__ = "learneds"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    student_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    lecture_id = Column(Integer, ForeignKey('lectures.id', ondelete='CASCADE'))
    custom_lecture_id = Column(Integer)
