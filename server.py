from routes import app


def start(debug=False):
    app.run(host="0.0.0.0", port=8080)
    app.debug = debug

