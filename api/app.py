from flask import Flask

app = Flask(__name__)

@app.router('/')
def hello():
    return 'Hello world'