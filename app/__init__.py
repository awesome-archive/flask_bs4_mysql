from flask import Flask
from flask_bootstrap import Bootstrap


bootstrap = Bootstrap



def create_app():
    app = Flask(__name__)
    bootstrap(app)

    app.config['SECRET_KEY'] = 'ff1!@#!alkk0909123'
    app.config['DEBUG'] = True
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


