from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, get_db
from app.services import dashboard_service

router=APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/income")
def get_total_income(db=Depends(get_db),current_user=Depends(get_current_user)):
	    return {"total_income": dashboard_service.get_total_income(db, current_user.id)}

@router.get("/expenses")
def get_total_expenses(db=Depends(get_db),current_user=Depends(get_current_user)):
		    return {"total_expenses": dashboard_service.get_total_expenses(db, current_user.id)}

@router.get("/balance")
def get_net_balance(db=Depends(get_db),current_user=Depends(get_current_user)):
		    return {"net_balance": dashboard_service.get_net_balance(db, current_user.id)}

@router.get("/categories")
def get_category_breakdown(db=Depends(get_db),current_user=Depends(get_current_user)):
		    return {"category_breakdown": dashboard_service.get_category_breakdown(db, current_user.id)}

@router.get("/monthly")
def get_monthly_summary(db=Depends(get_db),current_user=Depends(get_current_user)):
		    return {"monthly_summary": dashboard_service.get_monthly_summary(db, current_user.id)}
