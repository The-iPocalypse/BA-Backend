import json

from flask import Flask, Response, request
from database import get_database_connection

app = Flask(__name__)
app.debug = True


@app.route('/')
def home():
    with open('documentation.html', 'r') as doc:
        return doc.read()

@app.route('/users', methods=['GET'])
def users():
    connection = get_database_connection()

    try:
        with connection.cursor() as cursor:
            sql = "SELECT `id`, `username`, `name`, `picture`, `rating`, `description` FROM `Users`"
            cursor.execute(sql)
            result = cursor.fetchall()
            return Response(json.dumps(result, ensure_ascii=False, indent=2).encode('utf8'),  mimetype='application/json', content_type='application/json; charset=utf-8')
    finally:
        connection.close()


@app.route('/participations/<int:user_id>', methods=['GET'])
def user(user_id):
    connection = get_database_connection()

    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Participations INNER JOIN Good_Deeds ON Participations.good_deed_id = Good_Deeds.id WHERE Participations.user_id=%s"
            cursor.execute(sql, (user_id))
            result = cursor.fetchall()
            return Response(json.dumps(result, ensure_ascii=False, indent=2).encode('utf8'),  mimetype='application/json', content_type='application/json; charset=utf-8')
    finally:
        connection.close()


@app.route('/gooddeeds', methods=['POST'])
def gooddeeds():
    connection = get_database_connection()

    param_creator_user_id = request.form['creator-user-id']
    param_title = request.form['title']
    param_description = request.form['description']
    param_address = request.form['address']
    param_start_date = request.form['start-date']
    param_end_date = request.form['end-date']
    param_latitude = request.form['latitude']
    param_longitude = request.form['longitude']

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO Good_Deeds (title, description, address, start_date, end_date, creator_user_id, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (param_title, param_description, param_address, param_start_date, param_end_date,
                                 param_creator_user_id, param_latitude, param_longitude))

            connection.commit()
    finally:
        connection.close()

    return "", 200


@app.route('/gooddeeds-without-participation-ok', methods=['GET'])
def gooddeeds_without_participation_ok():
    connection = get_database_connection()

    try:
        with connection.cursor() as cursor:
            sql = "SELECT DISTINCT title, description, address, start_date, end_date, creator_user_id, latitude, longitude, Participations.status_id FROM Good_Deeds LEFT JOIN Participations ON Good_Deeds.id=Participations.good_deed_id WHERE Participations.status_id <> 1 OR Participations.status_id IS NULL"
            cursor.execute(sql)
            result = cursor.fetchall()
            return Response(json.dumps(result, ensure_ascii=False, indent=2).encode('utf8'),  mimetype='application/json', content_type='application/json; charset=utf-8')
    finally:
        connection.close()


@app.route('/participations', methods=['POST'])
def create_participation():
    connection = get_database_connection()

    param_user_id = request.form['user-id']
    param_deed_id = request.form['good-deed-id']

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO Participations (user_id, status_id, good_deed_id) VALUES (%s, %s, %s)"
            cursor.execute(sql, (param_user_id, 2, param_deed_id))
            connection.commit()
    finally:
        connection.close()

    return "", 200


@app.route('/participations_for_users_gooddeed/<int:user_id>', methods=['GET'])
def participations_for_users_gooddeed(user_id):
    connection = get_database_connection()

    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Participations INNER JOIN Good_Deeds ON Participations.good_deed_id = Good_Deeds.id WHERE Good_Deeds.creator_user_id =%s"
            cursor.execute(sql, (user_id))
            result = cursor.fetchall()
            return Response(json.dumps(result, ensure_ascii=False, indent=2).encode('utf8'),  mimetype='application/json', content_type='application/json; charset=utf-8')
    finally:
        connection.close()


@app.route('/accept_gooddeed_participation/<int:participation_id>', methods=['PUT'])
def accept_gooddeed_participation(participation_id):
    connection = get_database_connection()

    param_status_id = request.form['status-id']

    try:
        with connection.cursor() as cursor:
            sql = "UPDATE Participations SET status_id=%s WHERE Participations.id=%s"
            cursor.execute(sql, (param_status_id, participation_id))
            connection.commit()
    finally:
        connection.close()

    return "", 200

@app.route('/users/<int:user_id>', methods=['GET'])
def single_user(user_id):
    connection = get_database_connection()

    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Users WHERE Users.id=%s"
            cursor.execute(sql, (user_id))
            result = cursor.fetchall()
            return Response(json.dumps(result, ensure_ascii=False, indent=2).encode('utf8'),  mimetype='application/json', content_type='application/json; charset=utf-8')
    finally:
        connection.close()