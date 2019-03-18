# import json
# # d = {'name':'kobe','address':'luxi','age':'二十三'}
# # r = json.dump(d,open('d:/nice.txt','w'),ensure_ascii=False)
# # r2 = open('d:/nice.txt','r')
# # print(r2.read())
# #
# # res = json.load(open('d:/nice.txt','r'))
# # print(res)
# # print(type(res))
# class Student():
#     def __init__(self,name,age,score):
#         self.name = name
#         self.age = age
#         self.score = score
#         print('{0},{1},{2}'.format(name,age,score))
# def study(param):
#         return{
#             'age': param.age,
#             'name': param.name,
#             'score': param.score
#         }
# s = Student('kobe',23,12)
# print(json.dumps(s,default=study))
#
d1= {"num1": 111, "pwd1": 1111, "balance1": 10000}
d2 = {"num2": 222, "pwd2": 2222, "balance2": 20000}
d3 = {"num3": 333, "pwd3": 3333, "balance3": 30000}

def opreate():
    while True:
        n = int(input("1.取款，2.存款，3.退卡"))
        # isbreak = False
        if n == 2:
            mom = int(input("请输入你要存的金额"))
            if mom <= 0:
                print("存款金额必须大于0")
            else:
                Sum = mom + d["balance"]
                print("存款成功，余额为:", Sum)
        elif n == 1:
            out = int(input("请输入你要取的金额"))
            if out > d["balance"]:
                print("余额不足，请及时充钱！")
            else:
                sub = d["balance"] - out
                print("取款成功，取款金额为{0}，余额为".format(out), sub)
        elif n == 3:
            # isbreak = True
            # print("退卡成功")
            break
        else:
            print('没有此功能')
count = 0
while True:
    def login():
        card = int(input("请输入您的卡号"))
        pwd = int(input("请输入您的密码"))
        return card, pwd
    card, pwd = login()

    if int(card) == d1["num"] and int(pwd) == d1["pwd"]:
            opreate()
    else:
        count += 1
        if count < 3:
            print("密码错误！")
        else:
            print("冻结")
            break
















