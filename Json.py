import json
class Student():
    def __init__(self,name,age,score):
        self.name = name
        self.age = age
        self.score = score
s = Student('jones',22,23)
def student2dict(std):
     return {
    'name':std.name,
     'age' : std.age,
     'score':std.score
    }
print(json.dumps(s,default=student2dict))

# d = dict(name = 'Bob',age = 23, score = 33)
# print(json.dumps(d))
# json_str = '{"age":25,"name":"Kobe","socre":34}'
# print(json.loads(json_str))