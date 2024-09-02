from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(String, unique=True)
    chat_id =  Column(String)
    first_name = Column(String)
    last_name = Column(String)
    name_company = Column(String, nullable=True)
    start_time = Column(DateTime)
    last_update = Column(DateTime)

class SurveyResults(Base):
    __tablename__ = 'Survey Results'
    user_id = Column(Integer, primary_key=True)
    prifugovka = Column(Boolean, nullable=True)

def create_tables(Base=Base):
    engine = create_engine('sqlite:///datasets/bot_mkb.db')
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    return Session