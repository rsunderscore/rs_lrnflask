

class Config(object):
    POSTS_PER_PAGE=10


#secret key gen  = os.urandom(24)
#secret key is needed to use wtforms
class ProdConfig(Config):
    SECRET_KEY = b'5:\xb6p\'\xe3\xe6\x1d\xca_Z%\xc60\x0f\x08b\xfb\x98"\x85\x81\xacQ'

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI="sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True #needed to suppress FSADeprecation warning (significant overhead)
    SQLALCHEMY_ECHO = True
    SECRET_KEY = b'\xfe\x08\xf1I\xa1\x9a\x15\xfc\xd1j\xe5Q\x8e\xc6\x17q\xa9\xdd/\xf7\xe3\xf9\xc7\x0e'