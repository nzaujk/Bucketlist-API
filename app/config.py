
""" here we are specifying configurations for different
environments"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    ERROR_404_HELP = False


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    DATABASE_URL = "postgresql://postgres:root@localhost/bucketlist_db"


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:root@localhost/test_db"
    DEBUG = True
    # PRESERVE_CONTEXT_ON_EXCEPTION = False


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False

app_config = {
    'staging': StagingConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'parent': Config,
    'SECRET': os.getenv('SECRET')
}
