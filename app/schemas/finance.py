from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FinanceCreate(BaseModel):
	type:str
	amount:float
	category:str
	date:datetime
	description:Optional[str]=None

class FinanceUpdate(BaseModel):
	type:Optional[str]=None
	amount:Optional[float]=None
	category:Optional[str]=None
	date:Optional[datetime]=None
	description:Optional[str]=None

class FinanceResponse(BaseModel):
	id:int
	user_id:int
	type:str
	amount:float
	category:str
	date:datetime
	description:Optional[str]=None
	class Config:
		orm_mode=True