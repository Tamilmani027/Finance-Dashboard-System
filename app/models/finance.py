from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database import Base

class Finance(Base):
	__tablename__="finances"
	id=Column(Integer, primary_key=True, index=True)
	user_id=Column(Integer, ForeignKey("users.id"), index=True)
	type=Column(String(50), nullable=False )
	amount=Column(Float, nullable=False)
	category=Column(String(50), nullable=False)
	date=Column(DateTime, default=datetime.utcnow)
	description=Column(String(255), nullable=True)
	user=relationship("User")
