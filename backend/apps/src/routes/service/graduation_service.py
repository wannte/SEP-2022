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
        required = []
        non_required = []
        remain = []
        research = []
        for lecture in lectures:
            lecture_code = lecture.lecture_code
            if lecture.major == user_major:
                if lecture_code[2] == '9':
                    research.append(lecture)
                elif lecture.required:   
                    required.append(lecture)
                else:
                    non_required.append(lecture)
            else:
                remain.append(lecture)
        return {
            'required': required,
            'non_required': non_required,
            'research': research,
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
        language_sw = []
        required_ko = []
        required_en = []
        for lecture in lectures:
            if lecture.lecture_code in required_korean:
                if len(required_ko) == 0:
                    required_ko.append(lecture)
                else:
                    language_sw.append(lecture)
            elif lecture.lecture_code in required_english:
                if len(required_en) < 2:
                    required_en.append(lecture)
                else:
                    language_sw.append(lecture)
            elif lecture.lecture_code in choice_language_sw:
                language_sw.append(lecture)
            else:
                remain.append(lecture)
        return {
            'required_ko': required_ko,
            'required_en': required_en,
            'language_sw': language_sw,
        }, remain

    @staticmethod
    def basic(user_major: str, lectures: List[Lecture], db: Session):
        remain = []
        basic = []
        required_ma = []
        required_sc = []
        required_ba = []
        non_required_ba = []
        already_in = []
        for lecture in lectures:
            lecture_code = lecture.lecture_code
            if lecture_code in already_in:
                continue
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
                            already_in.append(experiment_lecture.lecture_code)
                            flag = True
                            break
                    if not flag:
                        basic.append(lecture)
                else:
                    basic.append(lecture)
            elif lecture_code in choice_basic:
                basic.append(lecture)
            elif lecture_code in required_basic:
                if lecture_code in required_basic_dict[user_major]:
                    required_ba.append(lecture)
                else:
                    non_required_ba.append(lecture)
            else:
                remain.append(lecture)
        required_sc_ = []
        for lecture, experiment in required_sc:
            if lecture.id == experiment.id:
                required_sc_.append(lecture)
            else:
                required_sc_ += [lecture, experiment]
        return {
            'required_ma': required_ma,
            'required_sc': required_sc_,
            'basic': basic,
            'required_ba': required_ba,
            'non_required_ba': non_required_ba,
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
            'other': other
        }