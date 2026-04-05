from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
	__tablename__="users"
	id=Column(Integer, primary_key=True, index=True)
	name=Column(String(50),  nullable=False)
	email=Column(String(50), index=True, unique=True, nullable=False)
	hashed_password=Column(String(300),  nullable=False)
	is_active=Column(Boolean, default=True)
	role_id=Column(Integer, ForeignKey("roles.id"), index=True)
	created_at=Column(DateTime, default=datetime.utcnow)
	roles=relationship("Role")

