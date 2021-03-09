import os


class Config:
    DEBUG = False
    SECRET_KEY = os.environ['SECRET_KEY']
    # TODO: input actual database URI for production mode
    # SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/shop'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # pagination
    ITEMS_PER_PAGE = 10

    # truncation of strings in templates
    NUMBER_OF_TRUNCATED_SYMBOLS = 100


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/shop'

