from sqlalchemy.orm import sessionmaker
from datasets.database import create_tables, User, SurveyResults
from utils import logger
import logging

Session = create_tables()
class DbComands:
    def __init__(self, Session:sessionmaker=Session, logger:logging=logger, create_logs:bool=True):
        self.Session = Session
        self.logger = logger
        self.logs = create_logs

    def add_user_to_base(self, user_data:dict) -> None:
        # sourcery skip: class-extract-method
        with self.Session() as session:
            new_user = User(
                chat_id=user_data['chat_id'],
                user_id=user_data['user_id'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                start_time=user_data['timestamp'],
                last_update=user_data['timestamp']
            )
            try:
                session.add(new_user)
                session.commit()
            except Exception as e:
                if self.logs:
                    self.logger.error(e)
                print(e)
                session.rollback()


    def update_user_name_company(self, user_id: int|str, user_data:dict) -> None:
        with self.Session() as session:
            try:
                if (
                    user := session.query(User)
                    .filter_by(user_id=str(user_id))
                    .first()
                ):
                    user.name_company = user_data['name_company']
                    user.last_update = user_data['timestamp']
                    session.commit()
            except Exception as e:
                if self.logs:
                    self.logger.error(e)
                print(e)
                session.rollback()