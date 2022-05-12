from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from apps.src.sql.database import get_db
from apps.src.sql.model import Learned, Lecture

rt = APIRouter(prefix='/data', tags=['data'])

@rt.get('/setting')
def setting(db: Session):
    for i in range(10):
        lecture_code = 'EC400'+str(i)
        newLecture = Lecture(lecture_code = lecture_code, lecture_name = '머신러닝과 딥러닝', year = '2022', semester = 'spring', required = False, major = 'EECS', credit = 3)
        db.add(newLecture)
    db.commit()
    return