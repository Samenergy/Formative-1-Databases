from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from config.database import Base
from sqlalchemy import Float
class CreditHistory(Base):
    __tablename__ = "credit_histories"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    credit_score = Column(Integer, nullable=False)
    cred_hist_length = Column(Float, nullable=False)
    previous_defaults = Column(String(5), nullable=False)  # "Yes" or "No"

    person = relationship("Person", back_populates="credit_history")