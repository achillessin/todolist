import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASEDIR, "todolist.db")


config = {
    "development": DevelopmentConfig
}