from sqlalchemy import func
from app.models.finance import Finance
from sqlalchemy.orm import Session
from fastapi import HTTPException

def get_total_income(db,user_id):
	record=db.query(func.sum(Finance.amount)).filter(Finance.user_id==user_id,Finance.type=="income").scalar()
	return record or 0
	
def get_total_expenses(db,user_id):
	record=db.query(func.sum(Finance.amount)).filter(Finance.user_id==user_id,Finance.type=="expense").scalar()
	return record or 0

def get_net_balance(db,user_id):
	income=get_total_income(db,user_id)
	expenses=get_total_expenses(db,user_id)
	net_balance=income - expenses
	return net_balance or 0

def get_category_breakdown(db,user_id):
	record=db.query(Finance.category, func.sum(Finance.amount))\
  .filter(Finance.user_id == user_id)\
  .group_by(Finance.category)\
  .all()
	return record or []

def get_monthly_summary(db,user_id):
	record=db.query(func.month(Finance.date), func.sum(Finance.amount))\
  .filter(Finance.user_id==user_id)\
  .group_by(func.month(Finance.date))\
  .all()
	return record or []
	