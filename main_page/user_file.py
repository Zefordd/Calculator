import os
from aiohttp import web
from aiohttp_session import get_session

from settings import BaseConfig
from models.user import User


class User_file(web.View):
    error = ''
    async def post(self):
        session = await get_session(self)
        if 'user' not in session:
            User_file.error = 'Please login to use this feature'
            location = self.app.router['index'].url_for()
            return web.HTTPFound(location=location)
        else:
            data = await self.post()
            user = session['user']
            user_file = data['user_file']

            with open(os.path.join(BaseConfig.STATIC_DIR + '/user_files/', user_file.filename), 'wb') as f:
                content = user_file.file.read()
                f.write(content)
                f.close()

            await User.save_user_file_url(user['login'], '/user_files/{}'.format(user_file.filename))

            location = self.app.router['index'].url_for()
            return web.HTTPFound(location=location)



            # data = await self.post()
            # login = session['user']['login']
            # user_file = data['user_file']
            # file_url = os.path.join('static\\user_files\\', user_file.filename)

            # with open(file_url, 'wb') as f:
            #     f.close()

            # await User.save_user_file_url(login, file_url)
            # location = self.app.router['index'].url_for()
            # return web.HTTPFound(location=location)