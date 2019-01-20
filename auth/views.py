from datetime import datetime
import aiohttp_jinja2

from aiohttp import web
from aiohttp_session import get_session


class Login(web.View):
    
    @aiohttp_jinja2.template('auth/login.html')
    async def get(self):
        session = await get_session(self)
        session['last_visit'] = str(datetime.utcnow())
        last_visit = "Last visited: " + session['last_visit']
        return dict(last_visit=last_visit)

    @aiohttp_jinja2.template('auth/login.html')
    async def post(self):
        data = await self.post()
        login = data['login']
        password = data['password']

        if login == 'admin' and password == 'admin':
            session = await get_session(self)
            user = dict(login=login, password=password)
            session['user'] = user
        else:
            exception = 'Invalid login or password, please enter admin admin'
            return dict(exception=exception)

        location = self.app.router['index'].url_for()
        return web.HTTPFound(location=location)


class Logout(web.View):
    async def get(self):
        session = await get_session(self)
        del session['user']
        location = self.app.router['index'].url_for()
        return web.HTTPFound(location=location)

