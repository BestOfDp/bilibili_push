import requests
from flask import Flask, request, jsonify
from flask_cors import *
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/getInfo/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        id = str(request.json['id'])
        url = 'http://my.lib.lsu.edu.cn/opac/item.php?marc_no=0000000000'
        url = url[:-len(id)] + id
        resp = requests.get(url)
        resp.encoding = 'utf8'
        soup = BeautifulSoup(resp.text, 'html.parser')
        books = soup.find_all('tr', class_='whitetext')
        json_data = []
        for book in books:
            book_data = {}
            datas = book.find_all('td')

            lis = ['t_index', 'number', 'year', 'place', 'available', 'back_place']
            for data, keys in zip(datas, lis):
                book_data[keys] = data.text
            for key in lis:
                if key not in book_data.keys():
                    book_data[key] = ''
            json_data.append(book_data)
        return jsonify(json_data)
    return 'YES'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
