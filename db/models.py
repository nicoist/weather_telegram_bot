from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, nullable=False, unique=True)
    city = Column(String, nullable=True)
    time = Column(String, nullable=True)

    def __repr__(self):
        return f"<User(id={self.telegram_id}, city={self.city}, time={self.time})>"

