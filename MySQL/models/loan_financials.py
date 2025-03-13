from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from config.database import Base

class LoanFinancials(Base):
    __tablename__ = "loan_financials"

    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loans.id"), nullable=False)
    interest_rate = Column(Float, nullable=False)
    percent_income = Column(Float, nullable=False)

    loan = relationship("Loan", back_populates="loan_financials")