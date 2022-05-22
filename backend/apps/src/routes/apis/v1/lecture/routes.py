from fastapi import APIRouter, Depends, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from apps.src.routes.service.learned_service import LearnedService
from apps.src.routes.service.lecture_service import LectureService
from apps.src.routes.service.user_service import get_user

from apps.src.sql.database import get_db
from apps.src.sql.model import Learned, Lecture, User

rt = APIRouter(prefix='/lectures', tags=['lecture'])

@rt.get('')
def get_lectures(year: str, semester: str, major: str, db: Session = Depends(get_db), user: User = Depends(get_user)):
    if not user:
        return JSONResponse(content={'ok': False, 'message': '없는 유저입니다.'}, status_code=401)
    lectures = LectureService.get_all_lectures_by_year_semester_major(year, semester, major, db)
    learned = LearnedService.get_all_learned_by_user_id(user.id, db)
    
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