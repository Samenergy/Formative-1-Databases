from fastapi import APIRouter, HTTPException
from controllers.controller import create_all_models, get_person, update_person, delete_person
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class LoanRequest(BaseModel):
    person_age: float
    person_gender: str
    person_education: str
    person_income: float
    person_emp_exp: int
    person_home_ownership: str
    loan_amnt: float
    loan_intent: str
    loan_int_rate: float
    loan_percent_income: float
    cb_person_cred_hist_length: float
    credit_score: int
    previous_loan_defaults_on_file: str
    loan_status: int

class PersonUpdateRequest(BaseModel):
    person_age: Optional[float] = None
    person_gender: Optional[str] = None
    person_education: Optional[str] = None
    person_income: Optional[float] = None
    person_emp_exp: Optional[int] = None
    person_home_ownership: Optional[str] = None
    loan_amnt: float
    loan_intent: str
    loan_int_rate: float
    loan_percent_income: float
    cb_person_cred_hist_length: float
    credit_score: int
    previous_loan_defaults_on_file: str
    loan_status: int


# CRUD Operations
@router.post("/crud/create-all")
async def crud_create_all(data: LoanRequest):
    return await create_all_models(data.dict())

@router.get("/crud/person/{person_id}")
async def crud_get_person(person_id: str):
    result = await get_person(person_id)
    if not result:
        raise HTTPException(status_code=404, detail="Person not found")
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.put("/crud/person/{person_id}")
async def crud_update_person(person_id: str, data: PersonUpdateRequest):
    result = await update_person(person_id, data.dict(exclude_unset=True))
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.delete("/crud/person/{person_id}")
async def crud_delete_person(person_id: str):
    result = await delete_person(person_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
