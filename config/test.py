import os

# Create the testing config
class Config():
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///test-food-recipe'