import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_SERVER = os.environ.get("DB_SERVER_DEVELOPMENT")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(
        os.path.join(BASE_DIR, DB_SERVER)
    )

    @property
    def DATABASE_URI(self):
        return self.SQLALCHEMY_DATABASE_URI


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_SERVER_PRODUCTION")


class DevelopmentConfig(Config):
    DB_SERVER = os.environ.get("DB_SERVER_DEVELOPMENT")
    DEBUG = True
