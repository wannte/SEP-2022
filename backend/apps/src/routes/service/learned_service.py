import pickle as p

from typing import List
from sqlalchemy.orm import Session
from apps.src.routes.service.user_service import UserService

from apps.src.sql.model import Learned, Lecture, User
from apps.src.common.code_list import *


class LearnedService():
    @staticmethod
    def get_learned_by_lecture_id_and_user_id(user_id: int, lecture_id: int,  db: Session) -> Learned:
        return db.query(Learned).filter(Learned.lecture_id == lecture_id).filter(Learned.student_id == user_id).first()

    @staticmethod
    def get_all_learned_lecture_by_user_id(user_id: int, db: Session):
        return db.query(Learned, Lecture).join(Lecture, Lecture.id == Learned.lecture_id) \
                        .filter(Learned.student_id == user_id).all()

    @staticmethod
    def get_learned_lecture_by_year_semester_user_id(year: str, semester: str, user_id: int, db: Session):
        return db.query(Learned, Lecture) \
            .join(Lecture, Learned.lecture_id == Lecture.id) \
            .filter(Learned.student_id == user_id) \
            .filter(Lecture.year == year) \
            .filter(Lecture.semester == semester) \
            .all()

    @staticmethod
    def get_all_learned_by_user_id(user_id: int, db: Session):
        return db.query(Learned) \
                .filter(Learned.student_id == user_id) \
                .all()


    @staticmethod
    def create_learned(user: User, lecture: Lecture, learned: Learned, db: Session):
        lecture_major = lecture.major
        lecture_code = lecture.lecture_code
        message = 'success'
        print('수강과목:',lecture.lecture_name)
        print('과목전공:',lecture_major)
        print('과목번호:',lecture_code)
        basic_lecture = p.loads(user.basic_lecture)
        non_credit_lecture = p.loads(user.non_credit_lecture)
        if lecture_major == 'GS':
            if lecture_code[2] == '0':
                # 예체능
                pass
            else:
                message = basic_lecture.add_lecture(lecture)
                user.basic_lecture = p.dumps(basic_lecture)
                # user.basic_lecture에 기초과목 추가하는 로직
        elif lecture.major == user.major:
            # 전공과목
            pass
        elif lecture_major == 'UC':
            # 콜로퀴움
            if lecture_code == 'UC9331':
                message = non_credit_lecture.add_lecture(lecture)
                user.non_credit_lecture = p.dumps(non_credit_lecture)
            # 봉사, 과기경
            pass
        else:
            # 타전공
            pass
        # 그외에도 과목이 어떤 것인지 판단하고 과목 추가하는 로직 필요
        UserService.update_user(user,db)
        try:
            db.add(learned)
            db.commit()
            return message
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def delete_learned(learned: Learned, db: Session):
        try:
            db.delete(learned)
            db.commit()
            return True
        except Exception as e:
            print(e)
            return False
    
    @staticmethod
    def delete_all_learned(learneds: List[Learned], db: Session):
        for learned in learneds:
            if not LearnedService.delete_learned(learned, db):
                return False
        return True