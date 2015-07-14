import os


basedir = os.path.abspath(os.path.dirname(__file__))
username = 'root'
password = 'mypassword'
host = 127.0.0.1
port = 3306
schema = 'myschema'
db_string = 'mysql://%s:%s@%s:%s/%s' %(username, password, host, port, schema)


class Config:
    SECRET_KEY = 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = db_string
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    @staticmethod
    def init_app(app):
            pass


class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
    }
