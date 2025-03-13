from sqlalchemy.orm import Session
from models.person import Person
from models.loan import Loan
from models.loan_financials import LoanFinancials
from models.credit_history import CreditHistory
from models.schemas import PersonCreate
from fastapi import HTTPException

def create_person_with_details(db: Session, person_data: PersonCreate):
    """Creates a new person along with their loan, financials, and credit history."""
    
    # Create Person instance
    new_person = Person(
        age=person_data.person_age,
        gender=person_data.person_gender,
        education=person_data.person_education,
        income=person_data.person_income,
        emp_exp=person_data.person_emp_exp,
        home_ownership=person_data.person_home_ownership,
    )
    db.add(new_person)
    db.commit()
    db.refresh(new_person)

    # Create Loan instance
    new_loan = Loan(
        person_id=new_person.id,
        loan_amount=person_data.loan_amnt,
        loan_intent=person_data.loan_intent,
        loan_status=person_data.loan_status,
    )
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)

    # Create Loan Financials instance
    new_loan_financials = LoanFinancials(
        loan_id=new_loan.id,
        interest_rate=person_data.loan_int_rate,
        percent_income=person_data.loan_percent_income,
    )
    db.add(new_loan_financials)
    db.commit()
    db.refresh(new_loan_financials)

    # Create Credit History instance
    new_credit_history = CreditHistory(
        person_id=new_person.id,
        credit_score=person_data.credit_score,
        cred_hist_length=person_data.cb_person_cred_hist_length,
        previous_defaults=person_data.previous_loan_defaults_on_file,
    )
    db.add(new_credit_history)
    db.commit()
    db.refresh(new_credit_history)

    return {
        "message": "Person and associated records created successfully",
        "person_id": new_person.id
    }

def get_person_with_details(db: Session, person_id: int):
    """Fetches a person and their related records."""
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    loans = db.query(Loan).filter(Loan.person_id == person_id).all()
    credit_history = db.query(CreditHistory).filter(CreditHistory.person_id == person_id).first()

    loan_data = []
    for loan in loans:
        loan_financials = db.query(LoanFinancials).filter(LoanFinancials.loan_id == loan.id).first()
        loan_data.append({
            "loan_id": loan.id,
            "loan_amount": loan.loan_amount,
            "loan_intent": loan.loan_intent,
            "loan_status": loan.loan_status,
            "loan_financials": {
                "interest_rate": loan_financials.interest_rate,
                "percent_income": loan_financials.percent_income,
            }
        })

    return {
        "person_id": person.id,
        "age": person.age,
        "gender": person.gender,
        "education": person.education,
        "income": person.income,
        "emp_exp": person.emp_exp,
        "home_ownership": person.home_ownership,
        "loans": loan_data,
        "credit_history": {
            "credit_score": credit_history.credit_score,
            "cred_hist_length": credit_history.cred_hist_length,
            "previous_defaults": credit_history.previous_defaults
        }
    }

def update_person(db: Session, person_id: int, person_data: PersonCreate):
    """Updates an existing person's details along with their related loan, financials, and credit history."""
    
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    # Update Person details
    person.age = person_data.person_age
    person.gender = person_data.person_gender
    person.education = person_data.person_education
    person.income = person_data.person_income
    person.emp_exp = person_data.person_emp_exp
    person.home_ownership = person_data.person_home_ownership
    db.commit()
    db.refresh(person)

    # Update Loan details
    loan = db.query(Loan).filter(Loan.person_id == person_id).first()
    if loan:
        loan.loan_amount = person_data.loan_amnt
        loan.loan_intent = person_data.loan_intent
        loan.loan_status = person_data.loan_status
        db.commit()
        db.refresh(loan)

        # Update Loan Financials
        loan_financials = db.query(LoanFinancials).filter(LoanFinancials.loan_id == loan.id).first()
        if loan_financials:
            loan_financials.interest_rate = person_data.loan_int_rate
            loan_financials.percent_income = person_data.loan_percent_income
            db.commit()
            db.refresh(loan_financials)

    # Update Credit History
    credit_history = db.query(CreditHistory).filter(CreditHistory.person_id == person_id).first()
    if credit_history:
        credit_history.credit_score = person_data.credit_score
        credit_history.cred_hist_length = person_data.cb_person_cred_hist_length
        credit_history.previous_defaults = person_data.previous_loan_defaults_on_file
        db.commit()
        db.refresh(credit_history)

    return {"message": f"Person with ID {person_id} updated successfully"}



def delete_person(db: Session, person_id: int):
    """Deletes a person and all related records."""
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    # Delete associated loan financials first
    loans = db.query(Loan).filter(Loan.person_id == person_id).all()
    for loan in loans:
        db.query(LoanFinancials).filter(LoanFinancials.loan_id == loan.id).delete()

    # Delete loans
    db.query(Loan).filter(Loan.person_id == person_id).delete()

    # Delete credit history
    db.query(CreditHistory).filter(CreditHistory.person_id == person_id).delete()

    # Finally, delete the person
    db.delete(person)
    db.commit()
    
    return {"message": f"Person with ID {person_id} and related records deleted successfully"}
