from aiohttp import web
import asyncio
from aiohttp_session import get_session
import aiohttp_jinja2
from settings import BaseConfig

from models.user import User, Customer, Item, Orders




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

class New_item(web.View):
    async def post(self):
        data = await self.post()
        item_name = data['item_name']
        cost = data['item_cost']
        description = data['item_description']
        item_img = data['item_img']
        file_name = '/item_imgs/' + item_name + '.' + item_img.filename.split('.')[-1]

        await Item.add_item(item_name, cost, file_name, description)

        item_img = data['item_img']
        try:
            file_path = BaseConfig.STATIC_DIR + file_name
            await User.save_user_file(file_path, item_img)
        except: pass
        print(item_img.filename)
        location = self.app.router['shop'].url_for()
        return web.HTTPFound(location=location)

class Items_info(web.View):
    async def get(self):
        items_info = await Item.get_items_info()
        return web.json_response(items_info)

class Customer_info(web.View):
    async def get(self):
        session = await get_session(self)
        if 'user' in session:
            login = session['user']['login']
            customer_info = await Customer.get_customer_data(login)
            return web.json_response(customer_info)



# out = {
#     'customer_login': login,
#     'current_balance': customer_data['balance'],
#     'customer_orders': customer_orders
# }