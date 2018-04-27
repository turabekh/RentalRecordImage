from flask import Flask
import os
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config



bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = os.path.join(APP_ROOT, 'static/')


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    


    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .dashboard import dashboard as dashboard_blueprint 
    app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')


    return app