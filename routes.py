from flask import Flask

app = Flask(__name__)
app.debug = True


@app.route('/')
def home():
    return "Hey ma gang de fous"
