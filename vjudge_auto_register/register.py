import requests
import uuid
from PIL import Image


class Register:
    def __init__(self):
        self.url = "https://cn.vjudge.net/user/register"  # 参数请求的url
        self.img_url = 'https://cn.vjudge.net/util/captcha?1539692289297.5'  # 获取验证码的url
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Ap'
                          'pleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
            'referer': 'referer: https://cn.vjudge.net/contest',
            # 'cookie': '_ga=GA1.2.807335439.1527913793; _gid=GA1.2.280053875.1539686618; JSESSIONID=70F1'
            #           '68F69C98B7654B6066BF85F229D6; _gat=1',
            'origin': 'https://cn.vjudge.net'
        }
        self.form = {
            'password': '123456',
            'repassword': '123456',
            'nickname': '',
            'school': '',
            'qq': '',
            'email': '2495088064@qq.com',
            'blog': '',
            'share': 1
        }

    def run(self, username):
        s = requests.session()
        self.form['username'] = username
        while True:
            img = s.get(self.img_url, stream=True, headers=self.headers)
            filename = uuid.uuid1().hex

            with open('{}.jpg'.format(filename), 'wb') as f:
                f.write(img.content)
            image = Image.open('{}.jpg'.format(filename))
            image.show()
            captcha = input("输入")
            self.form['captcha'] = captcha
            r = s.post(self.url, headers=self.headers, data=self.form)
            print(r.text)
            if r.text == 'success':
                break


if __name__ == '__main__':
    r = Register()
    for i in range(40, 55):
        id = str(i) if i >= 10 else "0" + str(i)
        r.run('lsuacm{}'.format(id))
