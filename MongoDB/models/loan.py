from pydantic import BaseModel
from typing import Optional

class Loan(BaseModel):
    loan_id: Optional[str] = None
    person_id: str
    loan_amnt: float
    loan_intent: str
    loan_status: int
