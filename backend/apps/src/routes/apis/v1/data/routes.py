import csv
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from apps.src.sql.database import get_db
from apps.src.sql.model import Learned, Lecture

rt = APIRouter(prefix='/data', tags=['data'])


def map_semester(korean_semester):
    d = {'1학기': 'spring', '여름학기': 'summer', '2학기': 'fall', '겨울학기': 'winter', '인정학기': '?'}
    return d[korean_semester]


def map_required(korean_required):
    return True if korean_required == '필수' else False


# TODO: Major mapping if required
def map_major(lecture_code_with_class):
    code = lecture_code_with_class[:2]
    return code


def extract_data(row):
    data = {
        'lecture_code': row['교과목-분반'][:6],
        'lecture_name': row['교과목명'],
        'year': row['년도'],
        'semester': map_semester(row['학기']),
        'required': map_required(row['이수\r구분']),
        'major': map_major(row["교과목-분반"]),
        'credit': row["강/실/학"][-1]
    }
    return data

import os
PATH = os.getcwd()

def get_data_from_csv():
    print(PATH)
    with open('{}/apps/src/routes/apis/v1/data/lectures~2022-1.csv'.format(PATH), newline='') as csvfile:
        lectures = []
        line_reader = csv.DictReader(csvfile, delimiter=',')
        for row in line_reader:
            extracted = extract_data(row)
            if extracted not in lectures:
                lectures.append(extracted)
    return lectures


@rt.get('/setting')
def setting(db: Session = Depends(get_db)):
    for i in range(10):
        lecture_code = 'EC400'+str(i)
        newLecture = Lecture(lecture_code = lecture_code, lecture_name = '머신러닝과 딥러닝', year = '2022', semester = 'spring', required = False, major = 'EECS', credit = 3)
        db.add(newLecture)
    db.commit()
    return

@rt.post('/csv')
def get_lecture_from_csv(db: Session = Depends(get_db)):
    db.query(Lecture).delete()
    lectures = get_data_from_csv()
    print(lectures[0])
    result = []
    for lecture in lectures:
        result.append(Lecture(lecture_code = lecture['lecture_code'], lecture_name = lecture['lecture_name'], year = lecture['year'], semester = lecture['semester'], required = lecture['required'], major = lecture['major'], credit = lecture['credit']))
    db.add_all(result)
    db.commit()
    count = db.query(Lecture).count()
    return {'ok': True, 'count': count}