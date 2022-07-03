import os
from dotenv import load_dotenv
load_dotenv(override=True)

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URI")
    FLASK_ENV= "development"
    # configuration variables for google authorization in development
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TESTING_DATABASE_URI")
    FLASK_ENV = "testing"

class ProductionConfig(Config):
    DEBUG = True
    # if os.getenv('PROD_DATABASE_URI'):
    SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DATABASE_URI").replace('postgres://','postgresql://')
    FLASK_ENV = "production"
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

class AzureConfig(Config):
    DEBUG = False
    # if os.getenv('PROD_DATABASE_URI'):
    SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DATABASE_URI").replace('postgres://','postgresql://')
    FLASK_ENV = "production"

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "azure": AzureConfig,
    "default": DevelopmentConfig
}

