import hashlib
from aiohttp_session import get_session

from sqlalchemy import create_engine

from sqlalchemy import Column, Integer, String, Float, ForeignKey, update

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref


engine = create_engine('sqlite:///my_db.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)
    file_url = Column(String, nullable=True)

    
    def __init__(self, login, password, file_url):
        self.login = login
        self.password = password
        self.file_url = file_url

    def __repr__(self):
        return "(login='%s', password='%s')" % (self.login, self.password)


    @staticmethod
    async def create_new_user(data):
        login = data['login']
        if session.query(User).filter(User.login==login).first():
            return dict(error='login is alreay in use')

        if data['login'] and data['password'] and data['password_2'] and data['password'] == data['password_2']:
            password = hashlib.sha256(data['password'].encode('utf8')).hexdigest()
            new_user = User(login, password, '')
            session.add(new_user)
            session.commit()
        else:
            return dict(error='wrong password or empty slot')

    @staticmethod
    async def get_user(login):
        if session.query(User).filter(User.login == login).first():
            password = session.query(User).filter(User.login == login).first().password
            file_url = session.query(User).filter(User.login == login).first().file_url
            login = session.query(User).filter(User.login == login).first().login
            return dict(login=login, password=password, file_url=file_url)

        return None

    @staticmethod
    async def save_user_file_url(login, file_url):
        session.query(User).filter(User.login == login).\
              update({"file_url": (file_url)})
        session.commit()


    @staticmethod
    async def save_user_file(file_path, user_file):
        with open(file_path, 'wb') as f:
            content = user_file.file.read()
            f.write(content)
            f.close()

    @staticmethod
    async def save_user_zip_file(file_path, zip_file_name):
        import zipfile
        with zipfile.ZipFile(file_path + '.zip', 'w') as zf:
            zf.write(zip_file_name, compress_type=zipfile.ZIP_DEFLATED)
            zf.close()

    @staticmethod
    async def get_delta_size(file_1,file_2):
        import os
        return(os.path.getsize(file_1) - os.path.getsize(file_2))



class Customer(User):
    balance = Column(Float)
    spent_money = Column(Float)
    items = Column(String)
    items_img = Column(String)

    def __init__(self, *args, **kwargs):
        super(Customer, self).__init__(*args, **kwargs)

    @staticmethod
    async def increase_balance(login, data):
        amount = float(data['amount'])
        current_balance = session.query(Customer).filter(Customer.login == login).first().balance
        total = amount + current_balance
        session.query(Customer.login == login).update({"balance": total})
        session.commit()

    @staticmethod
    async def get_customer_data(login):
        if session.query(Customer).filter(Customer.login == login).first():
            balance = session.query(Customer).filter(Customer.login == login).first().balance
            spent_money = session.query(Customer).filter(Customer.login == login).first().spent_money
            items = session.query(Customer).filter(Customer.login == login).first().items
            items_img = session.query(Customer).filter(Customer.login == login).first().items_img
            return dict(balance=balance, spent_money=spent_money, items=items, items_img=items_img)  


session.close()

"""
def add_column(engine, table_name, column):
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    engine.execute('ALTER TABLE %s ADD COLUMN %s %s' % (table_name, column_name, column_type))

Base.metadata.create_all(engine)  # создание таблицы

column = Column('file_url', String, primary_key=False)  # добавить новый столбец
add_column(engine, 'users', column)

"""
