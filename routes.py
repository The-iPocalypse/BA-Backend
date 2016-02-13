import json

from flask import Flask, Response, request
from database import get_database_connection

app = Flask(__name__)
app.debug = True


@app.route('/')
def home():
    return """
    <h1>Méthodes permises:</h1>

    <b><code>/users</b></code><br>
    Description: Retourne tous les utilisateurs<br>
    Méthode: GET<br><br>

    <b><code>/participations&lt;user_id&gt;</code></b><br>
    Description: Retourne toutes les bonnes actions auxquelles un utilisateur s'est inscrit<br>
    Méthode: GET<br><br>

    <b><code>/gooddeeds</code></b><br>
    Description: Permet l'ajout d'une bonne action<br>
    Méthode: POST<br>
    Paramètres:
    <ul>
        <li>creator-user-id</li>
        <li>title</li>
        <li>description</li>
        <li>address</li>
        <li>start-date</li>
        <li>end-date</li>
        <li>latitude</li>
        <li>longitude</li>
    </ul>

    <b><code>/gooddeeds-without-participation-ok</code></b><br>
    Description: Retourne toutes les bonnes actions qui n'ont pas reçu de postulations OU celles qui n'ont pas été encore acceptées (dont le statut n'est pas OK)<br>
    Méthode: GET<br><br>

    <b><code>/participations</code></b><br>
    Description: Permet l'ajout d'une participation. Le statut sera mis à Pending automatiquement<br>
    Méthode: POST<br>
    Paramètres:
    <ul>
        <li>user-id</li>
        <li>good-deed-id</li>
    </ul>

    <b><code>/participations_for_users_gooddeed/&lt;int:user_id&gt;</code></b><br>
    Description: Retourne la liste des personnes proposant leur aide à une bonne action pour un user préci<br>
    Méthode: GET<br><br>

    <b><code>/accept_gooddeed_participation/<int:participation_id>&lt;int:participation_id&gt;</code></b><br>
    Description: Applique le statut OK à une participation<br>
    Méthode: PUT<br><br>


    <b><code>/users/&lt;int:user_id&gt;</code></b><br>
    Description: Retrouve un utilisateur spécifique<br>
    Méthode: GET
    <ul>
        <li>status-id</li
    </ul>

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