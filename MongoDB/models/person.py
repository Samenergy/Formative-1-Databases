from pydantic import BaseModel
from typing import Optional

class Person(BaseModel):
    person_id: Optional[str] = None
    person_age: float
    person_gender: str
    person_education: str
    person_income: float
    person_emp_exp: int
    person_home_ownership: str
