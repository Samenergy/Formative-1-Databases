from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from config.database import Base

class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Float, nullable=False)
    gender = Column(String(10), nullable=False)
    education = Column(String(50), nullable=False)
    income = Column(Float, nullable=False)
    emp_exp = Column(Integer, nullable=False)
    home_ownership = Column(String(20), nullable=False)

    loans = relationship("Loan", back_populates="person")
    credit_history = relationship("CreditHistory", back_populates="person")