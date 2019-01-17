from datetime import datetime
import aiohttp_jinja2

from aiohttp import web
from aiohttp_session import get_session


class Index(web.View):
    @aiohttp_jinja2.template('calculator/index.html')
    async def get(self):
        session = await get_session(self)
        user = ''
        if 'user' in session:
            user = session['user']
        return dict(user=user)

class Feedback(web.View):
    @aiohttp_jinja2.template('feedback/feedback.html')
    async def get(self):
        pass
