from app.models.finance import Finance
from app.schemas.finance import FinanceCreate, FinanceUpdate
from fastapi import HTTPException
from sqlalchemy.orm import Session  

def create_record(db:Session,user_id,payload:FinanceCreate):
	record=Finance(user_id=user_id, **payload.dict())
	db.add(record)
	db.commit()
	db.refresh(record)
	return record

def get_all_records(db:Session, user_id):
	record=db.query(Finance).filter(Finance.user_id==user_id).all()
	return record

def get_record_by_id(db:Session,record_id,user_id):
	record=db.query(Finance).filter(Finance.id==record_id,Finance.user_id==user_id).first()
	if not record:
		raise HTTPException(status_code=404, detail="Record not found")
	return record

def update_record(db:Session,record_id,user_id,payload:FinanceUpdate):
	record=db.query(Finance).filter(Finance.id==record_id,Finance.user_id==user_id).first()
	if record:
		for field, value in payload.dict(exclude_unset=True).items():
			setattr(record, field, value)
	else:
		raise HTTPException(status_code=404)
	db.commit()
	db.refresh(record)
	return record


def delete_record(db:Session,record_id,user_id):
		record=db.query(Finance).filter(Finance.id==record_id,Finance.user_id==user_id).first()
		if record:
			db.delete(record)
			db.commit()
			return {"message":"Record deleted successfully"}
		else:
			raise HTTPException(status_code=404, detail="Record not found")

