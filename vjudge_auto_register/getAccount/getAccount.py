import json
import os
from flask import Flask, render_template, request

app = Flask(__name__)

a = 0


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/account', methods=['GET', 'POST'])
def account():
    global a
    a = a + 1
    if request.method == "POST":
        data = request.values
        info = dict()
        account = 'lsuacm2018'
        if a < 10:
            account = account + '0' + str(a)
        else:
            account = account + str(a)
        info['account'] = account
        info['classname'] = data['classname']
        info['username'] = data['username']
        info['school_id'] = data['school_id']
        info['qq'] = data['qq']
        json_str = json.dumps(info, ensure_ascii=False)
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/info.json')
        with open(path, 'a', encoding='utf-8') as f:
            f.write(json_str + ',\n')
        return render_template('account.html', info=info)

    return "YES"


if __name__ == '__main__':
    app.run()
