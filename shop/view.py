from aiohttp import web
from aiohttp_session import get_session
import aiohttp_jinja2

from models.user import User, Customer


class Shop(web.View):

    @aiohttp_jinja2.template('shop/shop.html')
    async def get(self):
        session = await get_session(self)
        if 'user' in session:
            login = session['user']['login']
            customer_data = await Customer.get_customer_data(login)
            customer_orders = await Customer.get_all_customer_orders(login)
            return dict(current_balance=customer_data['balance'],
                        customer_orders=customer_orders)
        else:
            return dict(current_balance='Please login to use the shop')

    async def post(self):
        session = await get_session(self)
        if 'user' not in session:
            location = self.app.router['login'].url_for()
            return web.HTTPFound(location=location)

        data = await self.post()
        login = session['user']['login']
        error = await Customer.increase_balance(login, data)
        if error:
            location = self.app.router['signup'].url_for()
            return web.HTTPFound(location=location)

        location = self.app.router['shop'].url_for()
        return web.HTTPFound(location=location)
