from typing import List
from fastapi import Depends, Header
from sqlalchemy.orm import Session

from apps.src.sql.database import get_db
from apps.src.sql.model import Lecture, User
from apps.src.common.code_list import *


class GraduationService():
    @staticmethod
    def liberal_arts(lectures: List[Lecture], db: Session):
        required = []
        select = []
        overflow = []
        remain = []
        for lecture in lectures:
            lecture_code = lecture.lecture_code
            if lecture_code in ppe + hus + gsc:
                if len(required) < 8:
                    required.append(lecture)
                elif len(select) < 4:
                    select.append(lecture)
                else:
                    overflow.append(lecture)
            else:
                remain.append(lecture)
        return {
            'required': required,
            'select': select,
            'overflow': overflow
        }, remain

    @staticmethod
    def major(user_major: str, lectures: List[Lecture], db: Session):
        major = []
        remain = []
        required = False
        for lecture in lectures:
            if lecture.major == user_major:
                if lecture.required:
                    required = True
                major.append(lecture)
            else:
                remain.append(lecture)
        sum_credit = sum(map(lambda x: x.credit, major))
        return {
            'major': major,
            'required': required,
            'sum_credit': sum_credit
        }, remain

    @staticmethod
    def other_major(user_major: str, lectures: List[Lecture], db: Session):
        remain = []
        other_major = []
        for lecture in lectures:
            if lecture.major not in ['GS', user_major, 'UC']:
                other_major.append(lecture)
            else:
                remain.append(lecture)
        sum_credit = sum(map(lambda x: x.credit, other_major))
        return {
            'other_major': other_major,
            'sum_credit': sum_credit
        }, remain
    
    @staticmethod
    def language(lectures: List[Lecture], db: Session):
        remain = []
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
            else:
                remain.append(lecture)
        return {
            'required_ko': required_ko,
            'required_en': required_en,
            'language': language,
        }, remain

    @staticmethod
    def basic(lectures: List[Lecture], db: Session):
        remain = []
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
            else:
                remain.append(lecture)
        return {
            'required_ma': required_ma,
            'required_sc': required_sc,
            'basic': basic,
        }, remain
    
    @staticmethod
    def other(lectures: List[Lecture], db: Session): 
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