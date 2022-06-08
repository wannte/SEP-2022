from sqlalchemy.orm import Session

from apps.src.sql.model import Learned, Lecture


class LectureService():
    @staticmethod
    def get_all_lectures_by_user_id(user_id: int, db: Session):
        lecture_learned = db.query(Learned, Lecture).join(Lecture, Lecture.id == Learned.lecture_id) \
                            .filter(Learned.student_id == user_id).order_by(Lecture.lecture_code).all()
        return list(map(lambda x: x.Lecture, lecture_learned))

    @staticmethod
    def get_all_lectures_order_by_year_by_user_id(user_id: int, db: Session):
        lectures = LectureService.get_all_lectures_by_user_id(user_id, db)
        lecture_dict = {}
        for lecture in lectures:
            year = lecture.year
            semester = lecture.semester
            if year not in lecture_dict:
                lecture_dict[year] = {semester: [lecture]}
                continue
            if semester not in lecture_dict[year]:
                lecture_dict[year][semester] = [lecture]
                continue
            lecture_dict[year][semester].append(lecture)
        return lecture_dict

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
        if (major=="ALL"):
            return db.query(Lecture) \
                .filter(Lecture.year == year) \
                .filter(Lecture.semester == semester) \
                .all()
        else: 
            return db.query(Lecture) \
                .filter(Lecture.major == major) \
                .filter(Lecture.year == year) \
                .filter(Lecture.semester == semester) \
                .all()

    @staticmethod
    def get_lecture_by_id(id: int, db: Session):
        return db.query(Lecture).filter(Lecture.id == id).first()