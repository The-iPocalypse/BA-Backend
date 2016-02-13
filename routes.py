import json

from flask import Flask, Response, request
from database import get_database_connection

app = Flask(__name__)
app.debug = True


@app.route('/')
def home():
    return """
    <h1>Méthodes permises:</h1>

    <b>/users</b><br>
    Description: Retourne tous les utilisateurs<br>
    Méthode: GET<br><br>

    <b>/participations<user_id></b><br>
    Description: Retourne toutes les bonnes actions auxquelles un utilisateur s'est inscrit<br>
    Méthode: GET<br><br>

    <b>/gooddeeds</b><br>
    Description: Permet l'ajout d'une bonne action<br>
    Méthode: POST<br><br>

    <b>/gooddeeds-without-participation-ok</b><br>
    Description: Retourne toutes les bonnes actions qui n'ont pas reçu de postulations OU celles qui n'ont pas été encore acceptées (dont le statut n'est pas OK)<br>
    Méthode: GET<br><br>

    """


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

    return "success"

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