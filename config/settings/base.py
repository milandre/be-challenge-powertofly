import os

basedir = os.path.abspath(os.path.join(__file__, '../../..'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'hard to guess string')
    SSL_REDIRECT = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # Example user
    EXAMPLE_EMAIL_USER = os.environ.get('EXAMPLE_EMAIL_USER', 'admin@example.com')

    # Redis config
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'RedisCache')
    CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL')
    """ CACHE_REDIS_HOST=os.environ.get('CACHE_HOST')
    CACHE_REDIS_PORT=os.environ.get('CACHE_PORT')
    CACHE_REDIS_DB=os.environ.get('CACHE_DB') """
    CACHE_DEFAULT_TIMEOUT = os.environ.get('CACHE_DEFAULT_TIMEOUT')

    @staticmethod
    def init_app(app):
        pass
