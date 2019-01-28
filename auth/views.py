import hashlib
import aiohttp_jinja2
from datetime import datetime

from aiohttp import web
from aiohttp_session import get_session

from models.user import User


class Login(web.View):
    error = ''

    @aiohttp_jinja2.template('auth/login.html')
    async def get(self):
        session = await get_session(self)
        session['last_visit'] = str(datetime.utcnow())
        last_visit = "Last visited: " + session['last_visit']
        return dict(last_visit=last_visit, error=Login.error)

    async def post(self):
        Login.error = ''
        data = await self.post()
        login = data['login']
        password = data['password']

        user = await User.get_user(login)
        if user and user['login'] == login and user['password'] == hashlib.sha256(password.encode('utf8')).hexdigest():
            session = await get_session(self)
            session['user'] = user
            location = self.app.router['index'].url_for()
            return web.HTTPFound(location=location)
        else:
            Login.error = 'Wrong login or password. Try again or use "admin admin"'
            return web.HTTPFound(location=self.app.router['login'].url_for())


class Logout(web.View):
    async def get(self):
        session = await get_session(self)
        del session['user']
        location = self.app.router['index'].url_for()
        return web.HTTPFound(location=location)


class Signup(web.View):

    @aiohttp_jinja2.template('auth/signup.html')
    async def get(self):
        return dict()

    async def post(self):
        data = await self.post()
        error = await User.create_new_user(data=data)
        if error:
            location = self.app.router['signup'].url_for()
            return web.HTTPFound(location=location)

        location = self.app.router['login'].url_for()
        return web.HTTPFound(location=location)
        



