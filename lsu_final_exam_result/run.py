import requests
import json
import xlrd
import time


class GetResult:
    def __init__(self, name, id, email):
        self.name = name
        self.id = id
        self.url = "http://weixiao.lsu.edu.cn/card/jw/getStudentExamResultListByXNandXQ"
        self.email = email

    def getScore(self):
        form_data = dict(
            shortCode=181,
            cardNumber=self.id,
            name=self.name
        )
        r_headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        s = requests.post(self.url, data=form_data, headers=r_headers)
        s.encoding = "utf-8"
        result = json.loads(s.text)
        result = result['data']['examResultList']
        return [dict(courseName=i['courseName'], grade=i['grade']) for i in result]

    def send_email(self, data):
        title = '出成绩啦！'
        msg = ""
        for i in data:
            msg += "课程名称{}:成绩{}".format(i['courseName'], i['grade'])
            msg += '\n'
        post_data = {
            'msg': msg,
            'title': title,
            'to': self.email
        }
		# 邮箱推送API
        requests.post('http://{}{}'.format(
            "xxxx", "xxx"),
            data=json.dumps(post_data))


if __name__ == '__main__':
    exc = xlrd.open_workbook('info.xls')
    table = exc.sheet_by_name("Sheet1")
    for i in range(81):
        name = table.cell_value(i + 5, 2)
        id = table.cell_value(i + 5, 1)
        peo = GetResult(name, id, "2")
        try:
            current_result = peo.getScore()
            for j in current_result:
                if j['courseName'] == '操作系统':
                    if int(j['grade']) < 60:
                        print(name, j['grade'])
                    break
        except Exception as e:
            print("wrong")
  
