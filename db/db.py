from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base
from config import DB_URL


# Creating connection of db
engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Func for creating all tables in db
def init_db():
    Base.metadata.create_all(bind=engine)

