import requests
import uuid
import json
from PIL import Image


class User:
    def __init__(self):
        self.s = requests.session()
        self.login_url = 'https://cn.vjudge.net/user/login'
        self.img_url = 'https://cn.vjudge.net/util/captcha?1539692289297.5'  # 获取验证码的url
        self.update_url = 'https://cn.vjudge.net/user/update'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Ap'
                          'pleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
            'referer': 'referer: https://cn.vjudge.net/contest',
            'origin': 'https://cn.vjudge.net',
        }

    def login(self, username, password):
        data = {
            'username': username,
            'password': password
        }
        result = self.s.post(self.login_url, headers=self.headers, data=data)
        if result.text == 'success':
            print(username + '登录成功')
        else:
            print(result.text)

    def update(self, info, password):
        data = {
            'email': "249508064@qq.com",
            'intro': "",
            'newpassword': "",
            'nickname': info,
            'password': password,
            'qq': "",
            'repassword': "",
            'school': "",
            'captcha': ""
        }
        while True:
            img = self.s.get(self.img_url, stream=True, headers=self.headers)
            filename = uuid.uuid1().hex

            with open('{}.jpg'.format(filename), 'wb') as f:
                f.write(img.content)
            image = Image.open('{}.jpg'.format(filename))
            image.show()
            captcha = input("输入")
            data['captcha'] = captcha
            data = json.dumps(data, ensure_ascii=False)
            headers = self.headers
            headers['content-type'] = 'application/json'
            r = self.s.post(self.update_url, headers=headers, data=data.encode('utf-8'))
            if r.text == '{}':
                print('修改成功')
                break

    def run(self, username, info, password='123456'):
        self.login(username, password)
        self.update(info, password)


if __name__ == '__main__':
    strings = ""
    with open("info.json", 'r', encoding='utf-8') as f:
        for line in f:
            strings = strings + line

    infos = json.loads(strings, encoding='utf-8')
    for st in infos:
        info = st['classname'] + st['username']
        user = User()
        user.run(st['account'], info)
