from flask import Flask
from flask_migrate import Migrate
from config import DevelopmentConfig
from app.models import db

# instance of migrate flask
migrate = Migrate()

def create_app(config=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    # initialize extension instances
    db.init_app(app)
    db.app = app

    # migrate initialization
    migrate.init_app(app, db)
    migrate.app = app

    return app
