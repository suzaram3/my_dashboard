from flask import Flask, render_template
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

login_manager = LoginManager()
login_manager.login_view = "auth.login"
mail = Mail()
moment = Moment()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from .book import book as book_blueprint

    app.register_blueprint(book_blueprint, url_prefix="/book")

    from .cont import cont as contact_blueprint

    app.register_blueprint(contact_blueprint, url_prefix="/contact")

    from .task import task as task_blueprint

    app.register_blueprint(task_blueprint, url_prefix="/task")

    return app
