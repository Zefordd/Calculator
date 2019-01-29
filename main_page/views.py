from datetime import datetime
import aiohttp_jinja2

from aiohttp import web
from aiohttp_session import get_session


class Index(web.View):

    @aiohttp_jinja2.template('main_page/index.html')
    async def get(self):
        spiral = Spiral.spiral
        return dict(spiral=spiral)


class Feedback(web.View):

    @aiohttp_jinja2.template('feedback/feedback.html')
    async def get(self):
        pass

class Metronome(web.View):

    @aiohttp_jinja2.template('metronome/metronome.html')
    async def get(self):
        pass


class Spiral(web.View):
    spiral = ''
    async def post(self):
        data = await self.post()
        Spiral.spiral =  await Spiral.make_spiral(data['dimension'])
        return web.HTTPFound(location=self.app.router['index'].url_for())
    
    @staticmethod
    async def make_spiral(n):
        if n == '0' or n == '':
            return 
        n = int(n)
        A = [[0 for i in range(n)]for j in range(n)]
        k = 1
        b = 0
        i,j = 0,0
        while A[i][j] <= n**2:
            i += b
            j += b
            for j in range(b,n): #top
                A[i][j] = k
                k += 1
            for i in range(b+1,n-1): #right
                A[i][j] = k
                k += 1
            i += 1
            for j in range(n-1,b,-1): #bot
                A[i][j] = k
                k += 1
            j = b
            for i in range(n-1,b,-1): #left
                A[i][j] = k
                k += 1
            b += 1
            n -= 1
            i,j = 0,0
        return A



