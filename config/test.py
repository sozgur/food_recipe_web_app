import os

# Create the testing config
class Config():
    SECRET_KEY = "asfasdfasdfasdfasdffd"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///test-food-recipe'
    SQLALCHEMY_ECHO = False
    WTF_CSRF_ENABLED = False
    