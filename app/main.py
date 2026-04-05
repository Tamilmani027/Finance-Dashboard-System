from fastapi import FastAPI
from app.database import SessionLocal,engine, Base
from app.models import user, role, finance
from app.routes.auth_routes import router as auth_router
from app.routes.finance_routes import router as finance_router


app=FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(finance_router)

@app.get("/")
def home_page():
	return {"message": "Welcome FastAPI"}



