# from selenium import webdriver
# from time import sleep
#
# driver = webdriver.Chrome()
# driver.get('http://www.baidu.com')
# sleep(1)
# driver.quit()
# driver.find_element_by_xpath('')
# driver.find_element_by_xpath('//*[@id="head_logo"]/div[1]/a[2]/img').click()
#driver.find_element_by_xpath('//*[@id="u_sp"]/a[5]').click()
# driver.find_element_by_link_text('贴吧').click()
# sleep(1)
#
# driver.find_element_by_link_text('高级搜索').click()
# sleep(2)
# driver.find_element_by_css_selector("[value='0']").click()
# sleep(2)
#
# driver.close()


d = {"num": 111, "pwd": 1111, "balance": 10000}


# while True:
def login():
    card = int(input("请输入您的卡号"))
    pwd = int(input("请输入您的密码"))
    return card, pwd


card, pwd = login()
count = 0
while True:
    if int(card) == d["num"] and int(pwd) == d["pwd"]:
        # print(d["balance"])

        while True:
            n = int(input("1.取款，2.存款，3.退卡"))
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
                print("退卡成功")


            else:
                print('去啥子钱喽，走，开黑去')
                break

    else:
        count += 1
        if count < 3:
            print("密码错误！")
            card = int(input("请输入您的卡号"))
            pwd = int(input("请输入您的密码"))
        else:
            print("冻结")
            break








