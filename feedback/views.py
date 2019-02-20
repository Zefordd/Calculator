from aiohttp import web
from aiohttp_session import get_session
import aiohttp_jinja2

from models.feedback import Feedback_model


class Feedback(web.View):
    result = ''
    @aiohttp_jinja2.template('feedback/feedback.html')

    async def get(self):
        Feedback.result = ''
        return dict(result=Feedback.result)


    async def post(self):
        data = await self.post()
        await Feedback_model.create_feedback(data)
        Feedback.result = "successful"

        location = self.app.router['feedback'].url_for()
        return web.HTTPFound(location=location)
