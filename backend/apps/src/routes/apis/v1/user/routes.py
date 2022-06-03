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

# @rt.get('')
# def test():
#     return {'ping': 'pong'}

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

# login
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
        student_id = student_id,
        major = major,
        basic_lecture = basic_lecture,
        non_credit_lecture = non_credit_lecture,
    )
    if not UserService.create_user(new_user, db):
        return JSONResponse(content={'ok': False, 'message': '유저 생성에 실패하였습니다.'}, status_code=400)
    return {'ok': True}

@rt.put('/major')
def change_major(major: str = Body(...) , user: User = Depends(get_user), db: Session = Depends(get_db)):
    user.major = major
    if not UserService.update_user(user, db):
        return JSONResponse(content={'ok': False, 'message': '전공 변경에 실패하였습니다.'}, status_code=400)
    return {'ok': True}

@rt.get('/info', description='해당 student_id의 정보')
def get_user_info(user: User = Depends(get_user), db: Session = Depends(get_db)):
    if not user:
        return JSONResponse(content={'ok': False, 'message': '없는 유저입니다.'}, status_code=401)
    return user

@rt.get('/lectures', description='해당 학기의 유저가 수강한 강의 목록')
def get_user_lectures(year: str, semester: str, user: User = Depends(get_user), db: Session = Depends(get_db)):
    if not user:
        return JSONResponse(content={'ok': False, 'message': '없는 유저입니다.'}, status_code=401)
    return LectureService.get_all_lectures_by_year_semester_user_id(year, semester, user.id, db)

@rt.post('/lectures/{lecture_id}')
def add_lecture(lecture_id: int, user: User = Depends(get_user), db: Session = Depends(get_db)):
    if not user:
        return JSONResponse(content={'ok': False, 'message': '없는 유저입니다.'}, status_code=401)
    lecture = LectureService.get_lecture_by_id(lecture_id, db)
    if not lecture:
        return JSONResponse(content={'ok': False, 'message': '없는 과목입니다.'}, status_code=400)
    if LearnedService.get_learned_by_lecture_id_and_user_id(user.id, lecture_id, db):
        return JSONResponse(content={'ok': False, 'message': '이미 등록된 과목입니다.'}, status_code=400)
    learned = Learned(student_id = user.id, lecture_id = lecture_id)
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

# def add() {
#     user.basic_science = "math={}, science: {}"
#     user.major = ""
#     usre.free_lecture = ""
# }

@rt.get('/lecture/liberal_arts')
def calculate_liberal_arts(user: User = Depends(get_user), db: Session = Depends(get_db)):
    if not user:
        return JSONResponse(content={'ok': False, 'message': '없는 유저입니다.'}, status_code=401)
    lectures = LectureService.get_all_lectures_by_user_id(user.id, db)
    required = []
    select = []
    overflow = []
    for lecture in lectures:
        if lecture in hus+ppe+gsc:
            if len(required) < 8:
                required.append(lecture)
            elif len(select) < 4:
                select.append(lecture)
            else:
                overflow.append(lecture)
    return {
        'required': required,
        'select': select,
        'overflow': overflow
    }

@rt.get('/lecture/major')
def calculate_major(user: User = Depends(get_user), db: Session = Depends(get_db)):
    if not user:
        return JSONResponse(content={'ok': False, 'message': '없는 유저입니다.'}, status_code=401)
    lectures = LectureService.get_all_lectures_by_user_id(user.id, db)
    major = []
    required = False
    for lecture in lectures:
        if lecture.major == user.major:
            if lecture.required:
                required = True
            major.append(lecture)
    sum_credit = sum(map(lambda x: x.credit, major))
    return {
        'major': major,
        'required': required,
        'sum_credit': sum_credit
    }

@rt.get('/lecture/other_major')
def calculate_other_major(user: User = Depends(get_user), db: Session = Depends(get_db)):
    if not user:
        return JSONResponse(content={'ok': False, 'message': '없는 유저입니다.'}, status_code=401)
    lectures = LectureService.get_all_lectures_by_user_id(user.id, db)
    other_major = []
    for lecture in lectures:
        if lecture.major not in ['GS', user.major, 'UC']:
            other_major.append(lecture)
    sum_credit = sum(map(lambda x: x.credit, other_major))
    return {
        'other_major': other_major,
        'sum_credit': sum_credit
    }

@rt.get('/lecture/language')
def calculate_language(user: User = Depends(get_user), db: Session = Depends(get_db)):
    if not user:
        return JSONResponse(content={'ok': False, 'message': '없는 유저입니다.'}, status_code=401)
    lectures = LectureService.get_all_lectures_by_user_id(user.id, db)
    language = []
    required_ko = []
    required_en = []
    for lecture in lectures:
        if lecture.lecture_code in required_korean:
            if len(required_ko) == 0:
                required_ko.append(lecture)
            else:
                language.append(lecture)
        elif lecture.lecture_code in required_english:
            if len(required_en) < 2:
                required_en.append(lecture)
            else:
                language.append(lecture)
        elif lecture.lecture_code in choice_language_sw:
            language.append(lecture)
    return {
        'required_ko': required_ko,
        'required_en': required_en,
        'language': language,
    }

@rt.get('/lecture/basic')
def calculate_basic(user: User = Depends(get_user), db: Session = Depends(get_db)):
    if not user:
        return JSONResponse(content={'ok': False, 'message': '없는 유저입니다.'}, status_code=401)
    lectures = LectureService.get_all_lectures_by_user_id(user.id, db)
    basic = []
    required_ma = []
    required_sc = []
    for lecture in lectures:
        lecture_code = lecture.lecture_code
        if lecture_code in required_math:
            if len(required_ma) < 2:
                required_ma.append(lecture)
            else:
                basic.append(lecture)
        elif lecture_code in required_science.keys():
            if len(required_sc) < 3:
                exp_code = required_science.get(lecture_code)
                flag = False
                for experiment_lecture in lectures:
                    if experiment_lecture.lecture_code == exp_code:
                        required_sc.append((lecture, experiment_lecture))
                        flag = True
                        break
                if not flag:
                    basic.append(lecture)
            else:
                basic.append(lecture)
        elif lecture_code in choice_basic:
            basic.append(lecture)
    return {
        'required_ma': required_ma,
        'required_sc': required_sc,
        'basic': basic,
    }

@rt.get('/lecture/other')
def calculate_other(user: User = Depends(get_user), db: Session = Depends(get_db)):
    if not user:
        return JSONResponse(content={'ok': False, 'message': '없는 유저입니다.'}, status_code=401)
    lectures = LectureService.get_all_lectures_by_user_id(user.id, db)
    freshman = []
    coloquium = []
    sport = []
    art_music = []
    other = []
    for lecture in lectures:
        lecture_code = lecture.lecture_code
        if lecture_code in freshman_semina:
            freshman.append(lecture)
        elif lecture_code == 'UC9331':
            coloquium.append(lecture)
        elif lecture_code[:4] == 'GS01':
            sport.append(lecture)
        elif lecture_code[:4] == 'GS02':
            art_music.append(lecture)
        else:
            other.append(lecture)
    return {
        'freshman': freshman,
        'coloquium': coloquium,
        'sport': sport,
        'art_music': art_music,
    }

# 졸업요건계산
@rt.get('/graduation2')
def can_i_graduate2(user: User = Depends(get_user), db: Session = Depends(get_db)):
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
        'liberal_arts': liberal_arts,
        'major': major,
        'other_major': other_major,
        'language': language,
        'basic': basic,
        'other': other,
    }

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
            'required_science': form_data(basic['required_ma']+basic['required_sc']),
            'required_language': form_data(language['required_ko']+language['required_en']),
            'liberal_arts': form_data(liberal_arts['required']),
            'freshman_semina': form_data(other['freshman'])
        },
        'major': {
            'reqruied': form_data(major['required']),
            'non_required': form_data(major['non_required'])
        },
        'research': {
            'research': form_data(major['research'])
        },
        'free_select':{
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