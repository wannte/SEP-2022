from fastapi import APIRouter, Body, Depends, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from apps.src.sql.database import get_db
from apps.src.sql.model import Learned, Lecture, User

rt = APIRouter(prefix='/users', tags=['user'])

@rt.get('')
def test():
    return {'ping': 'pong'}

@rt.get('/test')
def test_db(db: Session = Depends(get_db)):
    return {'ok': True}

# login
@rt.get('')
def check_user_exists(student_id: str, db: Session = Depends(get_db)):
    return db.query(User).filter(User.student_id == student_id).exists()

@rt.post('')
def sign_up(student_id: str = Body(...), major: str = Body(...), db: Session = Depends(get_db)):
    if db.query(User).filter(User.student_id == student_id).exists():
        return JSONResponse(content={'ok': False, 'message': '이미 존재하는 유저입니다.'}, status_code=400)
    user = User(student_id = student_id, major = major)
    db.add(user)
    db.commit()
    return {'ok': True}

@rt.put('/major')
def change_major(major: str = Body(...) , student_id: str = Header(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.student_id == student_id).first()
    user.major = major
    db.add(user)
    db.commit()
    return {'ok': True}

@rt.get('/lectures')
def get_user_lectures(year: str, semester: str, student_id: str = Header(...), db: Session = Depends(get_db)):
    learneds = db.query(Learned, Lecture) \
        .join(Learned.lecture_id == Lecture.id) \
        .filter(Learned.student_id == student_id) \
        .filter(Lecture.year == year) \
        .filter(Lecture.semester == semester) \
        .all()
    return list(map(lambda x: x.lecture, learneds))

@rt.post('/lectures/{lecture_id}')
def add_lecture(lecture_id: int, student_id: str = Header(...), db: Session = Depends(get_db)):
    if db.query(Learned).filter(Learned.lecture_id == lecture_id).filter(Learned.student_id == student_id).exists():
        return JSONResponse(content={'ok': False, 'message': '이미 등록된 과목입니다.'}, status_code=400)
    learned = Learned(student_id = student_id, lecture_id = lecture_id)
    db.add(learned)
    db.commit()
    return {'ok': True}

@rt.delete('/lectures/{lecture_id}')
def delete_lecture(lecture_id: int, student_id: str = Header(...), db: Session = Depends(get_db)):
    learned = db.query(Learned).filter(Learned.lecture_id == lecture_id).filter(Learned.student_id == student_id).first()
    if not learned:
        return JSONResponse(content={'ok': False, 'message': '등록되지 않은 과목입니다.'}, status_code=400)
    db.delete(learned)
    db.commit()
    return {'ok': True}