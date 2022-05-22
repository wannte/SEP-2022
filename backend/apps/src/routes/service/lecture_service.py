from sqlalchemy.orm import Session

from apps.src.sql.model import Learned, Lecture


class LectureService():
    @staticmethod
    def get_all_lectures_by_user_id(user_id: int, db: Session):
        lecture_learned = db.query(Learned, Lecture).join(Lecture, Lecture.id == Learned.lecture_id) \
                            .filter(Learned.student_id == user_id).all()
        return list(map(lambda x: x.Lecture, lecture_learned))

    @staticmethod
    def get_all_lectures_by_year_semester_user_id(year: str, semester: str, user_id: int, db: Session):
        learneds = db.query(Learned, Lecture) \
                    .join(Lecture, Learned.lecture_id == Lecture.id) \
                    .filter(Learned.student_id == user_id) \
                    .filter(Lecture.year == year) \
                    .filter(Lecture.semester == semester) \
                    .all()
        return list(map(lambda x: x.Lecture, learneds))

    @staticmethod
    def get_all_lectures_by_year_semester_major(year: str, semester: str, major: str, db: Session):
        return db.query(Lecture) \
                .filter(Lecture.major == major) \
                .filter(Lecture.year == year) \
                .filter(Lecture.semester == semester) \
                .all()