from sqlalchemy.orm import Session

from apps.src.sql.model import Learned, Lecture


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
    def create_learned(learned: Learned, db: Session):
        try:
            db.add(learned)
            db.commit()
            return True
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
    
