from fastapi import FastAPI
from app.database import SessionLocal,engine, Base
from app.models import user, role, finance

app=FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home_page():
	return {"message": "Welcome FastAPI"}


