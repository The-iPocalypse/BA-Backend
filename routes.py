import json

from flask import Flask, Response
import pymysql.cursors

app = Flask(__name__)
app.debug = True


@app.route('/')
def home():
    return 'API de iPocalypse'


@app.route('/users', methods=['GET'])
def users():
    connection = pymysql.connect(host='159.203.27.0',
                             user='root',
                             password='mz2v6BqKyw',
                             db='AMC',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            sql = "SELECT `id`, `username`, `name`, `picture`, `rating`, `description` FROM `Users`"
            cursor.execute(sql)
            result = cursor.fetchall()
            return Response(json.dumps(result, ensure_ascii=False, indent=2).encode('utf8'),  mimetype='application/json', content_type='application/json; charset=utf-8')
    finally:
        connection.close()