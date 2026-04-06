from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, get_db,require_admin,require_analyst,require_viewer
from app.schemas.finance import FinanceCreate,FinanceResponse,FinanceUpdate
from app.services import finance_service

router=APIRouter(prefix="/finance", tags=["Finance"])

@router.post("/", response_model=FinanceResponse)
def create(payload:FinanceCreate,db=Depends(get_db),current_user=Depends(require_analyst)):
	return finance_service.create_record(db,current_user.id,payload)

@router.get("/",response_model=list[FinanceResponse])
def get_all(db=Depends(get_db),current_user=Depends(require_viewer)):
	return finance_service.get_all_records(db,current_user.id)

@router.get("/{record_id}",response_model=FinanceResponse)
def get_single_record(record_id:int,db=Depends(get_db),current_user=Depends(require_viewer)):
	return finance_service.get_record_by_id(db,record_id,current_user.id)

@router.put("/{record_id}")
def update_record(record_id:int,payload:FinanceUpdate,db=Depends(get_db),current_user=Depends(require_analyst)):
	return finance_service.update_record(db,record_id,current_user.id,payload)

@router.delete("/{record_id}",response_model=dict)
def delete_record(record_id:int,db=Depends(get_db),current_user=Depends(require_admin)):
	return finance_service.delete_record(db,record_id,current_user.id)
