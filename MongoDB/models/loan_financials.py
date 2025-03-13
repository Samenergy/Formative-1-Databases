from pydantic import BaseModel
from typing import Optional

class LoanFinancials(BaseModel):
    finance_id: Optional[str] = None
    loan_id: str
    loan_int_rate: float
    loan_percent_income: float
