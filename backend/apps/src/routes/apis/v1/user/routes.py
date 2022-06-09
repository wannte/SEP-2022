import pickle as p
from typing import List
from fastapi import APIRouter, Body, Depends, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from apps.src.routes.service.user_service import UserService, get_user

from apps.src.sql.database import get_db
from apps.src.sql.model import Learned, Lecture, User
from apps.src.routes.apis.v1.user.item import *
from apps.src.routes.service.learned_service import LearnedService
from apps.src.routes.service.lecture_service import LectureService
from apps.src.routes.service.graduation_service import GraduationService

rt = APIRouter(prefix='/users', tags=['user'])

@rt.get('/test')
def test_db(db: Session = Depends(get_db)):
    return {'ok': True}


@rt.put('/reset')
def reset(user: User = Depends(get_user), db: Session = Depends(get_db)):
    user.basic_lecture = p.dumps(BasicLecture())
    user.non_credit_lecture = p.dumps(NonCreditLecture())
    UserService.update_user(user, db)
    learneds = LearnedService.get_all_learned_by_user_id(user.id, db)
    LearnedService.delete_all_learned(learneds, db)
    return {'ok': True}


@rt.get('')
def check_user_exists(student_id: str, db: Session = Depends(get_db)):
    user = UserService.get_user_by_student_id(student_id, db)
    if user:
        basic_lecture = p.loads(user.basic_lecture)
        non_credit_lecture = p.loads(user.non_credit_lecture)
        return {'basic_liberal_arts': basic_lecture, 'non_credit_required': non_credit_lecture}
    return False


@rt.post('')
def sign_up(student_id: str = Body(...), major: str = Body(...), db: Session = Depends(get_db)):
    if UserService.get_user_by_student_id(student_id, db):
        return JSONResponse(content={'ok': False, 'message': '이미 존재하는 유저입니다.'}, status_code=400)

    basic_lecture = p.dumps(BasicLecture())
    non_credit_lecture = p.dumps(NonCreditLecture())

    new_user = User(
        student_id=student_id,
        major=major,
        basic_lecture=basic_lecture,
        non_credit_lecture=non_credit_lecture,
    )
    if not UserService.create_user(new_user, db):
        return JSONResponse(content={'ok': False, 'message': '유저 생성에 실패하였습니다.'}, status_code=400)
    return {'ok': True}


@rt.put('/major')
def change_major(major: str = Body(...), user: User = Depends(get_user), db: Session = Depends(get_db)):
    user.major = major
    if not UserService.update_user(user, db):
        return JSONResponse(content={'ok': False, 'message': '전공 변경에 실패하였습니다.'}, status_code=400)
    return {'ok': True}


@rt.get('/info', description='해당 student_id의 정보')
def get_user_info(user: User = Depends(get_user), db: Session = Depends(get_db)):
    if not user:
        return JSONResponse(content={'ok': False, 'message': '없는 유저입니다.'}, status_code=401)
    return {
        'student_id': user.student_id,
        'major': user.major
    }

@rt.get('/lectures', description='해당 학기의 유저가 수강한 강의 목록')
def get_user_lectures(year: str, semester: str, user: User = Depends(get_user), db: Session = Depends(get_db)):
    if not user:
        return JSONResponse(content={'ok': False, 'message': '없는 유저입니다.'}, status_code=401)
    return LectureService.get_all_lectures_by_year_semester_user_id(year, semester, user.id, db)


@rt.get('/lectures/all', description="유저가 수강한 모든 강의 목록")
def get_user_all_lectures(user: User = Depends(get_user), db: Session = Depends(get_db)):
    if not user:
        return JSONResponse(content={'ok': False, 'message': '없는 유저입니다.'}, status_code=401)
    lecture = LectureService.get_all_lectures_order_by_year_by_user_id(user.id, db)
    if not lecture:
        return JSONResponse(content={'ok': False, 'message': '수강한 과목이 없습니다.'})
    return lecture


@rt.post('/lectures/{lecture_id}')
def add_lecture(lecture_id: int, user: User = Depends(get_user), db: Session = Depends(get_db)):
    if not user:
        return JSONResponse(content={'ok': False, 'message': '없는 유저입니다.'}, status_code=401)
    lecture = LectureService.get_lecture_by_id(lecture_id, db)
    if not lecture:
        return JSONResponse(content={'ok': False, 'message': '없는 과목입니다.'}, status_code=400)
    if LearnedService.get_learned_by_lecture_id_and_user_id(user.id, lecture_id, db):
        return JSONResponse(content={'ok': False, 'message': '이미 등록된 과목입니다.'}, status_code=400)
    learned = Learned(student_id=user.id, lecture_id=lecture_id)
    message = LearnedService.create_learned(user, lecture, learned, db)
    if not message:
        return JSONResponse(content={'ok': False, 'message': 'leanred 생성을 실패했습니다.'}, status_code=400)
    return {'ok': True, 'message': message}


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


@rt.delete('/lectures')
def delete_all_lectures(user: User = Depends(get_user), db: Session = Depends(get_db)):
    if not user:
        return JSONResponse(content={'ok': False, 'message': '없는 유저입니다.'}, status_code=401)
    learneds = LearnedService.get_all_learned_lecture_by_user_id(user.id, db)
    if not LearnedService.delete_all_learned(learneds, db):
        return JSONResponse(content={'ok': False, 'message': '수강 목록 전체 삭제에 실패했습니다.'}, status_code=400)
    return {'ok': True}


def form_data(lectures: List[Lecture]):
    credit = 0
    for lecture in lectures:
        credit += lecture.credit
    return {
        'lectures': lectures,
        'credit': credit
    }


@rt.get('/graduation')
def can_i_graduate(user: User = Depends(get_user), db: Session = Depends(get_db)):
    if not user:
        return JSONResponse(content={'ok': False, 'message': '없는 유저입니다.'}, status_code=401)
    lectures = LectureService.get_all_lectures_by_user_id(user.id, db)
    liberal_arts, lectures = GraduationService.liberal_arts(lectures, db)
    major, lectures = GraduationService.major(user.major, lectures, db)
    other_major, lectures = GraduationService.other_major(user.major, lectures, db)
    language, lectures = GraduationService.language(lectures, db)
    basic, lectures = GraduationService.basic(user.major, lectures, db)
    other = GraduationService.other(lectures, db)

    return {
        'basic': {
            'required_science': form_data(basic['required_ma'] + basic['required_sc']),
            'required_language': form_data(language['required_ko'] + language['required_en']),
            'liberal_arts': form_data(liberal_arts['required']),
            'freshman_semina': form_data(other['freshman'])
        },
        'major': {
            'required': form_data(major['required']),
            'non_required': form_data(major['non_required'])
        },
        'research': {
            'research': form_data(major['research'])
        },
        'free_select': {
            'liberal_arts': form_data(liberal_arts['select']),
            'language_sw': form_data(language['language_sw']),
            'pre_required': form_data(basic['required_ba']),
            'other_pre_required': form_data(basic['non_required_ba']),
            'basic': form_data(basic['basic']),
            'other_major': form_data(other_major['other_major']),
            'other': form_data(other['other'])
        },
        'non_credit': {
            'art_music': form_data(other['art_music']),
            'sport': form_data(other['sport']),
            'coloquium': form_data(other['coloquium']),
        }
    }
