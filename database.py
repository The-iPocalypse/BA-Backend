import pymysql

def get_database_connection():
    return pymysql.connect(host='159.203.27.0',
                           user='root',
                           password='mz2v6BqKyw',
                           db='AMC',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)