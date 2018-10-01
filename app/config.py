import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is to protect against CSRF'

    MYSQL_DATABASE_USER = 'root'
    MYSQL_DATABASE_PASSWORD = 'Placement@12'
    MYSQL_DATABASE_DB = 'trialDB'
    MYSQL_DATABASE_HOST = 'localhost'

    connectionURL = "mysql+pymysql://"+MYSQL_DATABASE_USER+":"+MYSQL_DATABASE_PASSWORD+"@"+MYSQL_DATABASE_HOST+"/"+MYSQL_DATABASE_DB

    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = connectionURL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
