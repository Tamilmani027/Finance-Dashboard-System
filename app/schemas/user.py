from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
	name:str
	email:EmailStr
	password:str
	role_id:int

class UserResponse(BaseModel):
	id:int
	name:str
	email:EmailStr
	is_active:bool
	role_id:int
	class Config:
		orm_mode=True
