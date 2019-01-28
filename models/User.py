from sqlalchemy import create_engine
engine = create_engine('sqlite:///my_db.db', echo=False)

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

#Base.metadata.create_all(engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)
    
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
            password = data['password']
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
