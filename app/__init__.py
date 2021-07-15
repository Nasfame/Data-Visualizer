from flask import Flask, jsonify
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()
DB_NAME = 'DB.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "Hiro"  # Cookies encrypted
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_ECHO'] = True  # Debug

    db.init_app(app)

    from app.models import Distribution, Distributor, Product, User

    with app.app_context():
        from .views import views
        from .auth import auth
        # db.drop_all()
        db.create_all()
        # dis1 = Distributor("DSS")
        # p1 = Product("FPS")
        # d1 = Distribution(2,2,"Ernakulam",1010,2021)
        # db.session.add_all([dis1, p1, d1])
        # db.session.commit()

        app.register_blueprint(views, url_prefix='/')
        app.register_blueprint(auth, url_prefix='/')

        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.route('/')
    def welcome():
        return jsonify("Welcome to Data Visualizer,Kindly Sign In")

    return app
