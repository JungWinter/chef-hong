import os
import pathlib

basedir = pathlib.Path(__file__).cwd()


class Config:
    APP_NAME = 'Chef Hong'

    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24))
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + str(basedir / 'data-dev.sqlite')

    @classmethod
    def init_app(cls, app):
        super().init_app(app)
        print('This is development config')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + str(basedir / 'data-test.sqlite')

    @classmethod
    def init_app(cls, app):
        super().init_app(app)
        print('This is testing config')


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + str(basedir / 'data.sqlite')
    SENTRY_DSN = os.environ.get('SENTRY_DSN')

    @classmethod
    def init_app(cls, app):
        super().init_app(app)
        print('BE CAREFUL! THIS IS PRODUCTION CONFIG!')
        assert os.environ.get('SENTRY_DSN'), 'SENTRY_DSN is not set'


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        super().init_app(app)

        # Log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    'unix': UnixConfig
}
