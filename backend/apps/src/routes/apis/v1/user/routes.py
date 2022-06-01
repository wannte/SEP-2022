from fastapi import APIRouter, Body, Depends, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from apps.src.routes.service.user_service import UserService, get_user

from apps.src.sql.database import get_db
from apps.src.sql.model import Learned, Lecture, User
from apps.src.routes.service.learned_service import LearnedService
from apps.src.routes.service.lecture_service import LectureService

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
    if UserService.get_user_by_student_id(student_id, db):
        return True
    return False

class NewUser():
    def __init__(self) -> None:
        pass
    def toJson(self):
        return 


@rt.post('')
def sign_up(student_id: str = Body(...), major: str = Body(...), db: Session = Depends(get_db)):
    if UserService.get_user_by_student_id(student_id, db):
        return JSONResponse(content={'ok': False, 'message': '이미 존재하는 유저입니다.'}, status_code=400)
    new_user = User(
        student_id = student_id,
        major = major,
        basic_lecture = 'basic_science={math={},science={}}'
    )
    if not UserService.create_user(User(student_id = student_id, major = major), db):
        return JSONResponse(content={'ok': False, 'message': '유저 생성에 실패하였습니다.'}, status_code=400)
    return {'ok': True}

@rt.put('/major')
def change_major(major: str = Body(...) , user: User = Depends(get_user), db: Session = Depends(get_db)):
    user.major = major
    if not UserService.update_user(user, db):
        return JSONResponse(content={'ok': False, 'message': '전공 변경에 실패하였습니다.'}, status_code=400)
    return {'ok': True}


@rt.get('/lectures', description='해당 학기의 유저가 수강한 강의 목록')
def get_user_lectures(year: str, semester: str, user: User = Depends(get_user), db: Session = Depends(get_db)):
    if not user:
        return JSONResponse(content={'ok': False, 'message': '없는 유저입니다.'}, status_code=401)
    return LectureService.get_all_lectures_by_year_semester_user_id(year, semester, user.id, db)

@rt.post('/lectures/{lecture_id}')
def add_lecture(lecture_id: int, user: User = Depends(get_user), db: Session = Depends(get_db)):
    if not user:
        return JSONResponse(content={'ok': False, 'message': '없는 유저입니다.'}, status_code=401)
    if LearnedService.get_learned_by_lecture_id_and_user_id(user.id, lecture_id, db):
        return JSONResponse(content={'ok': False, 'message': '이미 등록된 과목입니다.'}, status_code=400)
    learned = Learned(student_id = user.id, lecture_id = lecture_id)
    if not LearnedService.create_learned(learned, db):
        return JSONResponse(content={'ok': False, 'message': 'leanred 생성을 실패했습니다.'}, status_code=400)
    return {'ok': True}

@rt.delete('/lectures/{lecture_id}')
def delete_lecture(lecture_id: int, user: User = Depends(get_user), db: Session = Depends(get_db)):
    if not user:
        return JSONResponse(content={'ok': False, 'message': '없는 유저입니다.'}, status_code=401)
    learned = LearnedService.get_learned_by_lecture_id_and_user_id(user.id, lecture_id, db)
    if not learned:
        return JSONResponse(content={'ok': False, 'message': '등록되지 않은 과목입니다.'}, status_code=404)
    if not LearnedService.delete_learned(learned, db):
        return JSONResponse(content={'ok': False, 'message': 'learned 삭제를 실패했습니다.'}, status_code=400)
    return {'ok': True}

# year, semester를 고려할 것인가?
@rt.delete('/lectures')
def delete_all_lectures(user: User = Depends(get_user), db: Session = Depends(get_db)):
    if not user:
        return JSONResponse(content={'ok': False, 'message': '없는 유저입니다.'}, status_code=401)
    learneds = LearnedService.get_all_learned_lecture_by_user_id(user.id, db)
    if not LearnedService.delete_all_learned(learneds, db):
        return JSONResponse(content={'ok': False, 'message': '수강 목록 전체 삭제에 실패했습니다.'}, status_code=400)
    return {'ok': True}
    

@rt.get('/credit/total')
def count_all_credit(user: User = Depends(get_user), db: Session = Depends(get_db)):
    if not user:
        return JSONResponse(content={'ok': False, 'message': '없는 유저입니다.'}, status_code=401)
    lectures = LectureService.get_all_lectures_by_user_id(user.id, db)
    total_credit = 0
    for lecture in lectures:
        total_credit += lecture.credit
    return total_credit

# 졸업요건계산
@rt.get('/graduation')
def can_i_graduate(user: User = Depends(get_user), db: Session = Depends(get_db)):
    if not user:
        return JSONResponse(content={'ok': False, 'message': '없는 유저입니다.'}, status_code=401)
    if user.major != 'EC' or user.student_id[:4] not in ['2015', '2016', '2017']:
        return JSONResponse(content={'ok': False, 'message': 'EECS 전공 15, 16, 17학번만 가능합니다.'}, status_code=403)
    lectures = LectureService.get_all_lectures_by_user_id(user.id, db)
    # 기초과학: 수학 6학점, 물리/화학/생명/전컴 중 3과목 선택이수 + 물리/화학/생물 실험 동반 이수
    basic_math = ['GS1001', 'GS2001', 'GS2002', 'GS2003', 'GS2004']
    for lecture in lectures:
        if lecture.lecture_code in basic_math:
            return
    return {'ok': True}

# def add() {
#     user.basic_science = "math={}, science: {}"
#     user.major = ""
#     usre.free_lecture = ""
# }