import pathlib

class BaseConfig:

    debug = True
    app_name = 'Web calculator'
    secret_key = '234324235345234234234'

    PROJECT_ROOT = pathlib.Path(__file__).parent
    STATIC_DIR = str(PROJECT_ROOT /  'static')
