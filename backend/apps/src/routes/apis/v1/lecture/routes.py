from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from apps.src.sql.database import get_db
from apps.src.sql.model import Learned, Lecture

rt = APIRouter(prefix='/lectures', tags=['lecture'])

@rt.get('')
def get_lectures(year: str, semester: str, major: str, db: Session = Depends(get_db), student_id: str = Header(...)):
    lectures = db.query(Lecture) \
                .filter(Lecture.major == major) \
                .filter(Lecture.year == year) \
                .filter(Lecture.semester == semester) \
                .all()
    learned = db.query(Learned) \
                .filter(Learned.student_id == student_id) \
                .all()
    
    learned_ids = list(map(lambda x: x.lecture_id, learned))
    for lecture in lectures:
        lecture.learned = True if lecture.id in learned_ids else False
    return lectures

# @rt.get('')
# def test():
#     return {'ping': 'pong'}

# @rt.get('/test')
# def test_db(db: Session = Depends(get_db)):
#     return {'ok': True}