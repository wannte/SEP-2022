from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: int = Field(...)
    student_id: str = Field(..., min_length=8, max_length=8)
    major: str = Field(...)
    username: str = Field(...)
    password: str = Field(...)
    email: EmailStr = Field(...)
    total_credit: int = Field(..., default=0)
    class config:
        orm_mode = True

class Lecture(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    year: int
    semester: str
    code: str = Field(...)
    required: bool = Field(..., default=False)
    major: str = Field(...)
    course: str = Field(...)
    professor: str = Field(...)
    credit = int = Field(..., default=3)
    class config:
        orm_mode = True

class CustomLecture(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    year: int
    semester: str
    major: str = Field(...)
    course: str = Field(...)
    professor: str = Field(...)
    credit = int = Field(..., default=3)
    class config:
        orm_mode = True

class Learned(BaseModel):
    id: int = Field(...)
    student_id: int = Field(...)
    lecture_id: int
    custom_lecture_id: int
    class config:
        orm_mode = True
        