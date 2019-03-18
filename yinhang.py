class Card:

    def __init__(self,cid,pwd):

        self.cid = cid
        self.pwd = pwd
        self.money = 0
        self.islock = False
# 管理员类
class Admin:
    def __init__(self,name = 'admin',password = '123456'):
        self.name = name
        self.password = password

    def welcome(self):
        print('欢迎使用xx银行系统')

    #设置登录
    def login(self):
        name = input('请输入您的用户名:')
        password = input('请输入您的密码:')
        if name == self.name and password == self.password:
            return True
        else:
            return False

    #设置菜单界面
    def menu(self):
        print('建户【0】 销户【1】 查看余额【2】 存款【3】 取款【4】')
        print('转账【5】 锁卡【6】 解锁【7】 用户信息【8】 退出【9】')
# 用户类
import os
import pickle

class User:
    def __init__(self,name,uid,card):
        self.name = name
        self.uid = uid
        self.card = card

    def __str__(self):
        return '姓名:{} 身份证号:{} 银行卡:{}'.format(self.name,self.uid,self.card.cid)

    #保存用户信息到文件中
    @staticmethod
    def save_info(userinfo):
        #拼接要存放信息的目录
        pathname = os.path.join(os.getcwd(),'user_info.db')
        with open(pathname,'wb') as fp:
            pickle.dump(userinfo,fp)

    @staticmethod
    def load_info():
        pathname = os.path.join(os.getcwd(),'user_info.db')
        print(pathname)
        if os.path.exists(pathname):
            with open(pathname,'rb') as fp:
                ret = pickle.load(fp)
                print(ret)
                return ret

        else:
            return {}
# 银行系统功能类
# from help import Helper
# from user import User
# from card import Card

class Operate:
    def __init__(self,userinfo={}):
        self.userinfo = userinfo

    #设置银行系统的各种功能
    def new_user(self):
        name = input('请输入您的名字:')
        uid = input('请输入您的身份证号:')
        pwd = input('请输入您的银行卡密码:')
        #生成银行卡号
        cid = Helper.generate_card_cid()
        #加密银行卡密码
        pwd = Helper.encry_pwd(pwd)
        #创建银行卡和用户对象
        card = Card(cid,pwd)
        user = User(name,uid,card)
        self.userinfo[cid] = user
        #保存用户信息
        User.save_info(self.userinfo)
        print('开户成功!')

    def del_uesr(self):
        while True:
            cid = input('请输入您的银行卡号:')
            if cid:
                user = self.userinfo[cid]
                print(type(user))
                print(user.card)
                a = user.card
                print(type(a))
                count = 0
                while True:
                    pwd = input('请输入您的银行卡密码:')
                    if Helper.check_pwd(pwd,user.card.pwd):
                        del self.userinfo[cid]
                        User.save_info(self.userinfo)
                        break
                    else:
                        print('密码错误，请重新输入')
                        count += 1
                        if count >= 3:
                            print('密码错误次数上限')
            else:
                print('银行卡号不存在，请重新输入')

    def query_money(self):
        cid = input('请输入您的银行卡号:')
        user = self.userinfo[cid]
        print('金额:{}'.format(user.card.money))

    def save_money(self):
        cid = input('请输入您的银行卡号:')
        user = self.userinfo[cid]
        count = 0
        if user.card.islock:
            print('您的银行卡已冻结')
            return
        while True:
            pwd = input('请输入您的银行卡密码:')
            if Helper.check_pwd(pwd,user.card.pwd):
                money = int(input('请输入您要存入的金额:'))
                user.card.money += money
                User.save_info(self.userinfo)
                print('存款成功')
                break
            else:
                print('密码错误，请重新输入')
                count += 1
                if count >= 3:
                    print('密码错误次数已达上限')

    def get_money(self):
        cid = input('请输入您的银行卡号:')
        user = self.userinfo[cid]
        print(user)
        print(type(user))
        count = 0
        if user.card.islock:
            print('你的银行卡已冻结')
            return
        while True:
            pwd = input('请输入您的银行卡密码:')
            if Helper.check_pwd(pwd,user.card.pwd):
                money = int(input('请输入您要获取的金额:'))
                if user.card.money >= money:
                    user.card.money -= money
                    User.save_info(self.userinfo)
                    print('取款成功')
                    break
                else:
                    print('余额不足')
            else:
                print('密码错误,请重新输入')
                count += 1
                if count >= 3:
                    print('密码错误已达上限,银行卡已锁定')
                    user.card.islock = True
                    break
    #转账
    def give_money(self):
        cid = input('请输入您的银行卡号:')
        user = self.userinfo[cid]
        count = 0
        if user.card.islock:
            print('您的银行卡已冻结')
            return
        count = 0
        while True:
            pwd = input('请输入您的银行卡密码:')
            if Helper.check_pwd(pwd,user.card.pwd):
                cid1 = input('请输入您要转账的银行卡号:')
                user1 = self.userinfo[cid1]
                money = int(input('请输入您要转账的金额:'))
                user.card.money -= money
                user1.card.money += money
                User.save_info(self.userinfo)
                print('转账成功')
                break
            else:
                print('密码错误，请重新输入')
                count += 1
                if count >= 3:
                    print('密码错误次数已达上限，银行卡已锁定')
                    user.card.islock = True
    def lockcard(self):
        pass

    def nolock(self):
        cid = input('请输入您要解锁的银行卡号:')
        uid = input('请出示您的身份证:')
        user = self.userinfo[cid]
        # print(type(user))

        if user.uid == uid:
            user.card.islock = False
        else:
            print('身份证错误')

    def show(self):
        for i in self.userinfo:
            print(self.userinfo[i])
# 再建立一个help模块用于对卡号密码的创建
import hashlib
from random import randint

class Helper:

    @staticmethod
    #生成银行卡号
    def generate_card_cid(length=8):
        cid = ''
        for i in range(length):
            cid += str(randint(0,9))
        return cid

    #加密用户密码信息
    @staticmethod
    def encry_pwd(pwd):
        m = hashlib.md5()
        m.update(pwd.encode('utf-8'))
        return m.hexdigest()

    #核对用户信息
    @staticmethod
    def check_pwd(pwd,pwd_hash):
        m = hashlib.md5()
        m.update(pwd.encode('utf-8'))
        return m.hexdigest() == pwd_hash
# 银行系统运行代码
# from admin import Admin
# from operate import Operate
# from user import User
# from card import Card

#创建管理员对象
admin = Admin()
admin.welcome()
count = 0

while True:
    ret = admin.login()
    #加载用户信息
    userinfo = User.load_info()
    operate = Operate(userinfo)
    # print(type(userinfo))
    if ret:
        print('登录成功')
        while True:
            admin.menu()
            num = int(input('请输入您要进行的操作:'))
            isbreak = False
            if num == 0:
                operate.new_user()

            if num == 1:
                operate.del_uesr()

            if num == 2:
                operate.query_money()

            if num == 3:
                operate.save_money()

            if num == 4:
                operate.get_money()

            if num == 5:
                operate.give_money()

            if num == 6:
                operate.lockcard()

            if num == 7:
                operate.nolock()

            if num == 8:
                operate.show()

            if num == 9:
                isbreak = True
                break
            if isbreak == True:
                break

    else:
        print('密码错误，请重新输入')
        count += 1
        if count >= 3:
            print('密码错误上限')
            break