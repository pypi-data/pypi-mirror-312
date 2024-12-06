# -*- encoding: utf-8 -*-
import os, random, string, json

class Config(object):
    processes: int = os.environ.get('PROCESSES', 1)
    threaded: bool = os.environ.get('THREADED', True)
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = os.environ.get('PORT', 5000)

    SECRET_KEY="secret_sauce",
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict",

    #basedir = os.path.abspath(os.path.dirname(__file__))
    #get root
    basedir = os.getcwd()

    MEDIA_FOLDER = os.path.join(basedir, "media")
    # Assets Management
    ASSETS_ROOT = os.path.join(basedir, os.getenv('ASSETS_ROOT', 'static'))
    STATIC_FOLDER = os.getenv('STATIC_FOLDER', 'static')
    TEMPLATES_FOLDER = os.path.join(basedir, os.getenv('TEMPLATES_FOLDER', 'templates'))
    # Set up the App SECRET_KEY
    SECRET_KEY  = os.getenv('SECRET_KEY', None)
    if not SECRET_KEY:
        SECRET_KEY = ''.join(random.choice( string.ascii_lowercase  ) for i in range( 32 ))

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_ENGINE   = os.getenv('DB_ENGINE'   , None)
    DB_USERNAME = os.getenv('DB_USERNAME' , None)
    DB_PASS     = os.getenv('DB_PASS'     , None)
    DB_HOST     = os.getenv('DB_HOST'     , None)
    DB_PORT     = os.getenv('DB_PORT'     , None)
    DB_NAME     = os.getenv('DB_NAME'     , None)

    USE_SQLITE  = True

    # try to set up a Relational DBMS
    if DB_ENGINE and DB_NAME and DB_USERNAME:
        try:
            # Relational DBMS: PSQL, MySql
            SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
                DB_ENGINE,
                DB_USERNAME,
                DB_PASS,
                DB_HOST,
                DB_PORT,
                DB_NAME
            )

            USE_SQLITE  = False

        except Exception as e:

            print('> Error: DBMS Exception: ' + str(e) )
            print('> Fallback to SQLite ')


class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600


class DebugConfig(Config):
    DEBUG = True

config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
