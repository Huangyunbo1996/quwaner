from os import environ


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + environ.get('mysql_username') + ':' + \
                              environ.get('mysql_password') + '@localhost/quwaner_dev'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + environ.get('mysql_username') + ':' + \
                              environ.get('mysql_password') + '@localhost/quwaner_test'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + environ.get('mysql_username') + ':' + \
                              environ.get('mysql_password') + '@localhost/quwaner'


configs = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
