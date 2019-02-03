from sqlalchemy import create_engine

from sqlalchemy import Column, Integer, String, update

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///my_db.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Feedback_model(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    feedback_text = Column(String)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    phone = Column(Integer)
    
    def __init__(self, feedback_text, name, surname, email, phone):
        self.feedback_text = feedback_text
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone


    @staticmethod
    async def create_feedback(data):
        feedback_text = data['feedback_text']
        name = data['name']
        surname = data['surname']
        email = data['email']
        phone = data['phone']
        if feedback_text and name and surname and email:
            new_feedback = Feedback_model(feedback_text, name, surname, email, phone)
            session.add(new_feedback)
            session.commit()

    @staticmethod
    async def get_feedback(id):
        name = session.query(Feedback_model).filter(Feedback_model.id == id).first().name
        surname = session.query(Feedback_model).filter(Feedback_model.id == id).first().surname
        feedback_text = session.query(Feedback_model).filter(Feedback_model.id == id).first().feedback_text
        return dict(name=name, surname=surname, feedback_text=feedback_text, _id=id)
    
    @staticmethod
    def get_feedback_for_bot(id):
        name = session.query(Feedback_model).filter(Feedback_model.id == id).first().name
        surname = session.query(Feedback_model).filter(Feedback_model.id == id).first().surname
        feedback_text = session.query(Feedback_model).filter(Feedback_model.id == id).first().feedback_text
        return dict(name=name, surname=surname, feedback_text=feedback_text, _id=id)


session.close()

#Base.metadata.create_all(engine)