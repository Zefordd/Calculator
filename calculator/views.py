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


    @aiohttp_jinja2.template('calculator/index.html')
    async def post(self):
        data = await self.post()
        n = data['dem']
        n=5
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

        return dict(A=A)


    

class Feedback(web.View):
    @aiohttp_jinja2.template('feedback/feedback.html')
    async def get(self):
        session = await get_session(self)
        user = ''
        if 'user' in session:
            user = session['user']
        return dict(user=user)
