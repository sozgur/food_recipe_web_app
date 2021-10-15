import os


# Create the super class
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Create the development config
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///food-recipe'
    SQLALCHEMY_ECHO = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False


# Create the testing config
class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///test-food-recipe'

# create the production config
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')