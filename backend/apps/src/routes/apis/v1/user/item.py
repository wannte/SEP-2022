from pydantic import BaseModel, EmailStr, Field

from apps.src.common.code_list import *
from apps.src.sql.model import Lecture

# class User(BaseModel):
#     id: int = Field(...)
#     student_id: str = Field(..., min_length=8, max_length=8)
#     major: str = Field(...)
#     username: str = Field(...)
#     password: str = Field(...)
#     email: EmailStr = Field(...)
#     total_credit: int = Field(..., default=0)
#     class config:
#         orm_mode = True

# class Lecture(BaseModel):
#     id: int = Field(...)
#     name: str = Field(...)
#     year: int
#     semester: str
#     code: str = Field(...)
#     required: bool = Field(..., default=False)
#     major: str = Field(...)
#     course: str = Field(...)
#     professor: str = Field(...)
#     credit = int = Field(..., default=3)
#     class config:
#         orm_mode = True

# class CustomLecture(BaseModel):
#     id: int = Field(...)
#     name: str = Field(...)
#     year: int
#     semester: str
#     major: str = Field(...)
#     course: str = Field(...)
#     professor: str = Field(...)
#     credit = int = Field(..., default=3)
#     class config:
#         orm_mode = True

# class Learned(BaseModel):
#     id: int = Field(...)
#     student_id: int = Field(...)
#     lecture_id: int
#     custom_lecture_id: int
#     class config:
#         orm_mode = True


class BasicScience:
    def __init__(self):
        self.math = []
        self.science = {'물리': [], '화학': [], '생명': [], '전컴': []}
        self.credit = 0
        self.count_experiment = 0

    def add_math(self, math_code):
        if len(self.math) >= 2:
            return 0
        if math_code in self.math:
            return 0
        self.math.append(math_code)
        self.credit += 3
        return 3

    def add_science(self, key, course_code, experiment_code=None):
        if experiment_code or key == '전컴':
            self.count_experiment += 1
        if key not in self.science.keys():
            return 0
        if self.science[key]:
            return 0
        self.science[key] = [course_code, experiment_code]
        credit = 3 if key == '전컴' else 4
        self.credit += credit
        return credit

class BasicLanguage:
    def __init__(self):
        self.korean = None
        self.english = {1:None, 2:None}
        self.credit = 0
    
    def add_korean(self, korean_code):
        if self.korean:
            return False
        self.korean = korean_code
        self.credit += 3
        return 3
    
    def add_english(self, k, english_code):
        if english_code in required_english[k]:
            if self.english[k]:
                print('이미 영어 {}를 수강했습니다.'.format(k))
                return False
            self.english[k] = english_code
            self.credit += 2
        return 2

class BasicLecture:
    def __init__(self):
        self.basic_science = BasicScience()
        self.basic_language = BasicLanguage()
        self.freshman_semina = False
        self.credit = 0

    def add_lecture(self, lecture = Lecture, experiment_code=None):
        lecture_code = lecture.lecture_code
        language_result = self.add_basic_language(lecture_code)
        science_result = self.add_basic_science(lecture_code, experiment_code)
        freshman_result = self.add_freshman_semina(lecture_code)
        return "language: {}, science: {}, freshman: {}".format(language_result, science_result, freshman_result)


    def add_basic_science(self, lecture_code, experiment_code=None):
        math_code = ["GS1001","GS1011", "GS1012"]
        science_code = {'물리': ['GS1101', 'GS1103'], '화학': ['GS1201', 'GS1203'], '생명': ['GS1301'], '전컴': ['GS1401']}
        if lecture_code in math_code:
            credit = self.basic_science.add_math(lecture_code)
            self.credit += credit
            return '수학'
        for k,v in science_code.items():
            if lecture_code in v:
                credit = self.basic_science.add_science(k, lecture_code, experiment_code)
                self.credit += credit
                return k
        return 'X'

    def add_basic_language(self, lecture_code):
        credit = False
        if lecture_code in required_korean:
            credit = self.basic_language.add_korean(lecture_code)
        for k,v in required_english.items():
            if lecture_code in v:
                credit = self.basic_language.add_english(k, lecture_code)

        if not credit:
            if lecture_code in choice_language_sw:
                return '자유선택/언어선택으로 이동'
            return 'X'
        self.credit += credit
        return

    def add_freshman_semina(self, lecture_code):
        if lecture_code in freshman_semina and not self.freshman_semina:
            self.freshman_semina = True
            self.credit += 1
            return 'O'
        return 'X'

class NonCreditLecture:
    def __init__(self):
        self.art_music = []
        self.sport = []
        self.coloquium = []
    
    def add_art_music(self, lecture_id):
        if len(self.art_music) > 3:
            return '초과'
        if lecture_id in self.art_music:
            return '이미 수강'
        self.art_music.append(lecture_id)
        return 'O'
    
    def add_sport(self, lecture_id):
        if len(self.sport) > 3:
            return '초과'
        if lecture_id in self.sport:
            return '이미 수강'
        self.sport.append(lecture_id)
        return 'O'

    def add_coloquium(self, lecture_id):
        if lecture_id in self.coloquium:
            return '이미 수강'
        self.coloquium.append(lecture_id)
        return 'O'
    
    def add_lecture(self, lecture = Lecture):
        lecture_id = lecture.id
        lecture_code = lecture.lecture_code
        if lecture_code[3] == 1:
            result = self.add_sport(lecture_id)
            return '체능 {}'.format(result)
        if lecture_code[3] == 2:
            result = self.add_art_music(lecture_id)
            return '예능 {}'.format(result)
        if lecture_code == 'UC9331':
            result = self.add_coloquium(lecture_id)
            return '콜로퀴움 {}'.format(result)
        return 'X'