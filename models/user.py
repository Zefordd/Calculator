import hashlib

from sqlalchemy import create_engine

from sqlalchemy import Column, Integer, String, update

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///my_db.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)
    file_url = Column(String)
    
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def __repr__(self):
        return "(login='%s', password='%s')" % (self.login, self.password)


    @staticmethod
    async def create_new_user(data):
        login = data['login']
        if session.query(User).filter(User.login==login).first():
            return dict(error='login is alreay in use')

        if data['login'] and data['password'] and data['password_2'] and data['password'] == data['password_2']:
            password = hashlib.sha256(data['password'].encode('utf8')).hexdigest()
            new_user = User(login, password)
            session.add(new_user)
            session.commit()
        else:
            return dict(error='wrong password or empty slot')


    @staticmethod
    async def get_user(login):
        if session.query(User).filter(User.login == login).first():
            login = session.query(User).filter(User.login == login).first().login
            password = session.query(User).filter(User.login == login).first().password
            return dict(login=login, password=password)

        return None

    @staticmethod
    async def save_user_file_url(login, file_url):
        session.query(User).filter(User.login == login).\
              update({"file_url": (file_url)})
        session.commit()



def add_column(engine, table_name, column):
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    engine.execute('ALTER TABLE %s ADD COLUMN %s %s' % (table_name, column_name, column_type))



session.close()
"""

Base.metadata.create_all(engine)  # создание таблицы

column = Column('file_url', String, primary_key=False)  # добавить новый столбец
add_column(engine, 'users', column)

"""
