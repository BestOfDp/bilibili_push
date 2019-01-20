import requests
import uuid
from bs4 import BeautifulSoup
from train.check import check
from PIL import Image


class LsuSpider:
    def __init__(self, user_id, password):
        self.login_url = 'http://jwgl.lsu.edu.cn/default2.aspx'
        self.payload = {
            '__VIEWSTATE': '',
            'txtUserName': str(user_id),
            'Textbox1': '',
            'TextBox2': str(password),
            'txtSecretCode': '',
            'RadioButtonList1': '(unable to decode value)',
            'Button1': '',
            'lbLanguage': '',
            'hidPdrs': '',
            'hidsc': '',
        }
        self.headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        self.check_code = 'http://jwgl.lsu.edu.cn/CheckCode.aspx'
        self.s = None

    def run(self):
        self._get_session()
        self._set_VIEWSTATE()
        self._login()

    def _set_validate_code(self):
        img = self.s.get(self.check_code, stream=True, headers=self.headers)
        filename = uuid.uuid1().hex

        with open('login_code/{}.jpg'.format(filename), 'wb') as f:
            f.write(img.content)
        image = Image.open('login_code/{}.jpg'.format(filename))
        self.payload['txtSecretCode'] = check(image)

    def _login(self):
        while True:
            self._set_validate_code()
            post1 = self.s.post(self.login_url, data=self.payload, headers=self.headers)
            if post1.status_code != 200:
                print('失败')
            if post1.url == 'http://jwgl.lsu.edu.cn/xs_main.aspx?xh=' \
                            '{}'.format(self.payload['txtUserName']):
                print('成功')
                break
            else:
                print('失败')

    def _get_session(self):
        s = requests.Session()
        self.s = s

    def _set_VIEWSTATE(self):
        response = self.s.get(self.login_url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        hidden = soup.find('input', type='hidden').attrs['value']
        self.payload['__VIEWSTATE'] = hidden


if __name__ == '__main__':
    lsu = LsuSpider('xxx', 'xxx')
    lsu.run()
