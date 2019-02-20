import os
from aiohttp import web
from aiohttp_session import get_session

from settings import BaseConfig
from models.user import User
from . import user_file



class User_file(web.View):
    error = ''
    delta_size = ''
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
                    os.remove(BaseConfig.STATIC_DIR + user['file_url'] + '.zip')
                except: pass

            user_file = data['user_file']
            try:
                file_path = BaseConfig.STATIC_DIR + '/user_files/' + user['login'] + '_' + user_file.filename
                await User.save_user_file(file_path, user_file)

                os.chdir(BaseConfig.STATIC_DIR + '/user_files/')
                zip_file_name = user['login'] + '_' + user_file.filename
                await User.save_user_zip_file(file_path, zip_file_name)

                User_file.delta_size = await User.get_delta_size(file_path, file_path + '.zip') 
            except AttributeError:
                User_file.error = "Choose your file"

            if data['user_file']:
                user_file_name = '/user_files/{}_{}'.format(user['login'], user_file.filename)
                await User.save_user_file_url(user['login'], user_file_name)
                user = {'login': user['login'], 'password': user['password'], 'file_url': user_file_name}
                session['user'] = user
            
            location = self.app.router['index'].url_for()
            return web.HTTPFound(location=location)
