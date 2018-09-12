import json
import requests
import pymysql
from contextlib import contextmanager


class Bili:
    def __init__(self, bid, email):
        self.query_sql = 'select * from Up'
        self.friends_url = 'https://api.bilibili.com/x/relation/' \
                           'followings?vmid={}&pn=1&ps=50&or' \
                           'der=desc&jsonp=jsonp&callback=__jp6'.format(bid)
        self.headers = {
            'referer': "https://space.bilibili.com/{}".format(bid),
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit'
                          '/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
        }
        self.up_url = "https://space.bilibili.com/ajax/member/ge" \
                      "tSubmitVideos?mid={}&page=1&pagesize=1"
        self.old_friends = {}
        self.new_friends = {}
        self.email_message = []
        self.email = email

    def __enter__(self):
        self.conn = pymysql.connect(
            host='xxx',
            user='xxx',
            password='xxx',
            database='bilibili',
            charset='utf8'
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query_sql)
        self.old_friends_data = self.cursor.fetchall()
        for id, title, author, created in self.old_friends_data:
            self.old_friends[id] = [id, title, author, created]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            print(exc_val)
        self.cursor.close()
        self.conn.close()
        return True

    def run(self):
        friends = self._get_friends()['data']['list']
        for friend in friends:
            mid = friend['mid']
            uname = friend['uname']
            up = requests.get(self.up_url.format(mid), headers=self.headers)
            info = json.loads(up.text)
            info = info['data']['vlist']
            if info:
                title = info[0]['title']
                created = info[0]['created']
                self.new_friends[mid] = [mid, title, uname, str(created)]
        self._judge_is_new()
        if len(self.email_message) != 0:
            self._send_email()

    def _judge_is_new(self):
        for key, value in self.old_friends.items():
            if not self.new_friends.__contains__(key):
                self._delete_friend(value[0])
            else:
                if value[3] != self.new_friends[key][3]:
                    self._update_friends(self.new_friends[key])
                self.new_friends.pop(key)
        self._add_new_friends()

    def _delete_friend(self, mid):
        with self._auto_commit():
            delete_sql = 'delete from Up WHERE id={}'.format(mid)
            self.cursor.execute(delete_sql)

    def _add_new_friends(self):
        with self._auto_commit():
            for id, title, author, created in self.new_friends.values():
                insert_sql = "insert into Up VALUES ({},'{}','{}','{}')".format(id, title, author, created)
                self.cursor.execute(insert_sql)

    def _update_friends(self, value):
        with self._auto_commit():
            update_sql = "update Up set " \
                         "title='{}'," \
                         "author='{}'," \
                         "created='{}'" \
                         "WHERE id={}".format(value[1], value[2], value[3], value[0])
            self.cursor.execute(update_sql)
            self.email_message.append(value)

    def _get_friends(self):
        data = requests.get(self.friends_url, headers=self.headers)
        return json.loads(data.text[6:-1])

    def _send_email(self):
        data = list(zip(*self.email_message))
        msg = '更新了！\n'
        title = ','.join(data[2])
        msg = msg + '\n'.join(data[1])
        post_data = {
            'msg': msg,
            'title': title,
            'to': self.email
        }
        requests.post('http://xxx/send_email/', data=json.dumps(post_data))

    @contextmanager
    def _auto_commit(self):
        try:
            yield
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()


if __name__ == '__main__':
    with Bili('你的bid', '你的email') as b:
        b.run()
