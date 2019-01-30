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
            if user['file_url'] and data['user_file']:
                try:
                    await User.save_user_file_url(user['login'], '')
                    os.remove(BaseConfig.STATIC_DIR + user['file_url'])
                except: pass

            user_file = data['user_file']            
            try:
                with open(os.path.join(BaseConfig.STATIC_DIR + '/user_files/',
                    user['login'] + '_' + user_file.filename), 'wb') as f:
                    content = user_file.file.read()
                    f.write(content)
                    f.close()
            except AttributeError:
                User_file.error = "Choose your file"

            if data['user_file']:
                user_file_name = '/user_files/{}_{}'.format(user['login'], user_file.filename)
                await User.save_user_file_url(user['login'], user_file_name)
                user = {'login': user['login'], 'password': user['password'], 'file_url': user_file_name}
                session['user'] = user


            location = self.app.router['index'].url_for()
            return web.HTTPFound(location=location)
