from passlib.context import CryptContext
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from jose import jwt
from datetime import datetime,timedelta

pwd_context=CryptContext(schemes=["bcrypt"])

def hash_password(password:str):
	return pwd_context.hash(password)

def verify_password(password: str, hashed:str):
	return pwd_context.verify(password,hashed)

def create_access_token(data):
	payload={
		"exp": datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
		"iat": datetime.utcnow(),
	}
	payload.update(data)
	token=jwt.encode(payload,SECRET_KEY, algorithm=ALGORITHM)
	return token
