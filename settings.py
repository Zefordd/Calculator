import pathlib

class BaseConfig:

    debug = True
    app_name = 'Web calculator'
    secret_key = '234324235345234234234'
    database_uri = 'postgresql://localhost:8080/p_db'

    PROJECT_ROOT = pathlib.Path(__file__).parent
    STATIC_DIR = str(PROJECT_ROOT /  'static')
