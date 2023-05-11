import os
import time

basedir = os.path.abspath(os.path.dirname(__file__))
# os.environ['TZ'] = 'Europe/Sofia'
# time.tzset()
print(time.strftime('%X %x %Z'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATION = False
