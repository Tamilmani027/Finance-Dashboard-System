from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings

db_url=f"mysql+mysqlconnector://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:3306/{settings.DB_NAME}"
engine=create_engine(db_url)
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()

