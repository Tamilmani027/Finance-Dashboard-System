import os
from dotenv import load_dotenv

load_dotenv()

DB_USER=os.getenv("DB_USER")
DB_PASS=os.getenv("DB_PASS")
DB_HOST=os.getenv("DB_HOST")
DB_NAME=os.getenv("DB_NAME")
DB_PORT=os.getenv("DB_PORT")
ALGORITHM=os.getenv("ALGORITHM")
SECRET_KEY=os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


