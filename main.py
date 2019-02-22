import base64
import logging

import aiohttp_jinja2
import asyncpgsa
import jinja2
from aiohttp import web
from aiohttp_session import setup, get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet

from routes import setup_routes, setup_static_routes
from settings import BaseConfig


async def current_user(request):
    session = await get_session(request)
    user = None
    if 'user' in session:
        user = session['user']

    return dict(user=user)


def main():
    app = web.Application(debug=True)

    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup(app, EncryptedCookieStorage(secret_key))

    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader(package_name='main', package_path='templates'),
        context_processors=[current_user])

    setup_routes(app)
    setup_static_routes(app)
    app['static_root_url'] = '/static'

    app['config'] = BaseConfig
    logging.basicConfig(level=logging.DEBUG)

    web.run_app(app, host='0.0.0.0', port=8080)


async def on_start(app):
    config = app['config']
    app['db'] = await asyncpgsa.create_pool(dsn=config['database_uri'])


async def on_shutdown(app):
    await app['db'].close()


if __name__ == '__main__':
    main()
