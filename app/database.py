from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import DB_USER, DB_PASS, DB_HOST, DB_NAME

db_url=f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}"
engine=create_engine(db_url)
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()

