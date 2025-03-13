from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from config.database import Base
class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    loan_amount = Column(Float, nullable=False)
    loan_intent = Column(String(50), nullable=False)
    loan_status = Column(Integer, nullable=False)  # 1 = Approved, 0 = Rejected

    person = relationship("Person", back_populates="loans")
    loan_financials = relationship("LoanFinancials", back_populates="loan") 