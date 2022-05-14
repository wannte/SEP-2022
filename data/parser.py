import csv


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


with open('lectures~2022-1.csv', newline='') as csvfile:
    lectures = []
    lecture_codes = set()
    line_reader = csv.DictReader(csvfile, delimiter=',')
    for row in line_reader:
        extracted = extract_data(row)
        if extracted not in lectures:
            lectures.append(extracted)
            lecture_codes.add(extracted['major'])

    print(line_reader.fieldnames)
    print(lecture_codes)
    print(len(lectures))
    for lecture in lectures:
        print(lecture)
