from os import environ


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '%dfsa@$%./'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + environ.get('mysql_username') + ':' + \
                              environ.get('mysql_password') + '@localhost/quwaner_dev'
    MAIL_USERNAME = environ.get('quwaner_email_username')
    MAIL_PASSWORD = environ.get('quwaner_email_password')
    MAIL_DEFAULT_SENDER = environ.get('quwaner_email_username')
    MAIL_USE_SSL = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_SUBJECT_PREFIX = '<趣玩儿> '

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
