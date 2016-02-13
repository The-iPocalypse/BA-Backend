import json

from flask import Flask, Response
from database import get_database_connection

app = Flask(__name__)
app.debug = True


@app.route('/')
def home():
    return """
    <h1>Méthodes permises:</h1>

    <b>/users</b><br>
    Description: Retourne tous les utilisateurs<br><br>

    <b>/participations/<user_id></b><br>
    Description: Retourne toutes les bonnes actions auxquelles un utilisateur s'est inscrit<br>



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

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
       if hasattr(obj, 'isoformat'):
           return obj.isoformat()
       else:
           return json.JSONEncoder.default(self, obj)


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