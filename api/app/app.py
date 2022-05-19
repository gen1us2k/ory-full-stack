from flask import Flask

def create_app(testing=False):
    app = Flask(__name__)
    app.config.from_object("config.settings")
    return app

