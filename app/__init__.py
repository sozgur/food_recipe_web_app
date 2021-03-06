import os
from flask import Flask
from flask_migrate import Migrate
from app.models import db
from app.models import login_manager
from flask_mail import Mail



# instance of migrate flask
migrate = Migrate()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(f"config.{os.environ['FLASK_ENV']}.Config")

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

    from app.test import test as test_blueprint
    app.register_blueprint(test_blueprint)

    return app
