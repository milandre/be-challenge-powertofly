import os

from .base import Config


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite://'
    WTF_CSRF_ENABLED = False

    @classmethod
    def init_app(cls, app):
        print(
            'THIS APP IS IN TESTING MODE.  \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.'
        )
