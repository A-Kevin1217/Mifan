import threading
import time
import requests
import hashlib


class Mifan(object):
    def __init__(self, userid, password):
        self.acc = userid
        self.pwd = password
        self.session = requests.session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) '
                          'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Content - Type': 'application / x - www - form - urlencoded;charset = UTF - 8'
        }
        self.login()

    def login(self):
        data = {
            'gid': '689',
            'uid': self.acc,
            'password': geneartemd5(self.pwd),
            'tad': '',
            'encrypt': 'true'
        }
        vall = self.session.post(url='https://mifan.61.com/api/v1/login', data=data)
        try:
            temp = vall.json()['data']
        except KeyError:
            temp = '登录成功'
        print(time.strftime("%H:%M:%S"), self.acc, temp)

    def sign(self):
        url = 'https://mifan.61.com/api/v1/event/dailysign/'
        value = self.session.get(url=url)
        return value.json()['data']


def geneartemd5(strs):
    """
    生成MD5

    :param strs: 要加密的字符串
    :return 加密后的MD5值
    """
    hl = hashlib.md5()
    hl.update(strs.encode(encoding='utf-8'))
    return hl.hexdigest()


def submit_sign(acc, pwd):
    """
    签到子方法

    :param acc: 账号
    :param pwd: 密码
    """
    signs = Mifan(acc, pwd).sign()
    print(time.strftime("%H:%M:%S"), acc, signs)


def book_seat(list_form):
    """
    多账号多线程支持

    :param list_form: 账号 密码
    """
    ths = []
    for index in list_form:
        ths.append(
            threading.Thread(target=submit_sign,
                             args=(index[0], index[1]))
        )
    for th in ths:
        th.start()
    for th in ths:
        th.join()


def main_handler():
    user_data = [  # 账号 密码
        ['******', '******']
    ]
    a = time.time()
    book_seat(user_data)  # 立刻预约
    b = time.time()
    end_time = time.strftime("%H:%M:%S")
    print(end_time, f'执行时长:{round(b - a, 4)}s')


if __name__ == '__main__':
    main_handler()
