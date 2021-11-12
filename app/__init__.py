from flask import Flask
from flask_migrate import Migrate
from config import DevelopmentConfig, ProductionConfig, TestingConfig

from app.models import db
from app.models import login_manager
from flask_mail import Mail


# instance of migrate flask
migrate = Migrate()
mail = Mail()

def create_app(config=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    # initialize extension instances
    db.init_app(app)
    db.app = app

    # migrate initialization
    migrate.init_app(app, db)
    migrate.app = app

    # login manager initialization
    login_manager.init_app(app)
    login_manager.app = app

    #mail initialization
    mail.init_app(app)
    mail.app = app

    from app.category import category as category_blueprint
    app.register_blueprint(category_blueprint)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    from app.recipe import recipe as recipe_blueprint
    app.register_blueprint(recipe_blueprint)


    return app
