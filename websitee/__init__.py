from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database11.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'red five diamonds in my bag'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .userava import userava

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(userava, url_prefix='/')

    from .models import User, Note, Userava
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')