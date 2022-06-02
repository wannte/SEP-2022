from pydantic import BaseModel, EmailStr, Field


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

    def add_math(self, math_code):
        if len(self.math) >= 2:
            return False
        if math_code in self.math:
            return "error"
        self.math.append(math_code)
        self.credit += 3
        return True

    def add_science(self, key, course_code, experiment_code=None):
        if key not in self.science.keys():
            return False
        if self.science[key]:
            return False
        self.science[key] = [course_code, experiment_code]
        credit = 3 if key == '전컴' else 4
        self.credit += credit
        return True


class BasicLecture:
    def __init__(self):
        self.basic_science = BasicScience()

    def add_basic_science(self, lecture_code, experiment_code=None):
        math_code = ["GS1011", "GS1012"]
        science_code = {'물리': ['GS1101', 'GS1103'], '화학': ['GS1201', 'GS1203'], '생명': ['GS1301'], '전컴': ['GS1401']}
        if lecture_code in math_code:
            self.basic_science.add_math(lecture_code)
            return
        for (k, v) in science_code.items():
            if lecture_code in v:
                self.basic_science.add_science(k, lecture_code, experiment_code)
                return

        