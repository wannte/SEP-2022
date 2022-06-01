import json


# class ComplexEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if hasattr(obj, 'toJSON'):
#             return obj.toJSON()
#         else:
#             return json.JSONEncoder.default(self, obj)

class BasicScience:
    def __init__(self):
        self.math = []
        self.science = {'물리': [], '화학': [], '생명': [], '전컴': []}
        self.credit = 0
    #
    # def toJSON(self):
    #     return dict(math=self.math, science=self.science)

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
    #
    # def toJSON(self):
    #     return dict(basic_science=self.basic_science)

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


a = BasicLecture()
a.add_basic_science("GS1011")
a.add_basic_science("GS1012")
a.add_basic_science("GS1101", 'GS1103')
a.add_basic_science("GS1201", 'GS1203')
a.add_basic_science("GS1401")

# print(json.dumps(a.toJSON(), cls=ComplexEncoder, ensure_ascii=False))

import pickle
x = pickle.dumps(a)
bl = pickle.loads(x)
print(bl)

# a_string = '{"math": ["GS1011", "GS1012"], "science": {"물리": ["GS1101", "GS1103"], "화학": ["GS1201", "GS1203"], "생명": [], "전컴": ["GS1401", null]}}'
# b = json.loads(a_string)
# bl = BasicLecture(**b)
#
# print(bl)
