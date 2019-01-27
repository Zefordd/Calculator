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

    @staticmethod
    async def create_new_user(data):
        login = data['login']
        if login in  session.query(User).filter(User.login==login).first().login:
            err = 'login alreay in use'
            return dict(err=err)
        if data['login'] and data['password'] and data['password_2'] and data['password'] == data['password_2']:
            password = data['password']
            new_user = User(login, password)
            session.add(new_user)
            session.commit()

    @staticmethod
    def create_new_user_test(log, pas, pas_2):
        if session.query(User).filter(User.login==log).first():
            err = 'login alreay in use'
            return print(err)

        if log and pas and pas == pas_2:
            new_user = User(log, pas)
            session.add(new_user)
            session.commit()
        else:
            print('wrong password or empty slot')




