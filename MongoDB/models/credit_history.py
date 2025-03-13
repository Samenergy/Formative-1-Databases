from pydantic import BaseModel
from typing import Optional

class CreditHistory(BaseModel):
    credit_id: Optional[str] = None
    person_id: str
    credit_score: int
    cb_person_cred_hist_length: float
    previous_loan_defaults_on_file: str
