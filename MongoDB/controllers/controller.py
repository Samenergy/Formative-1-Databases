from config.db import database
from bson import ObjectId
import numpy as np
from pymongo import MongoClient
import pickle
import tensorflow as tf
from tensorflow.keras.models import load_model
from config.db import collection
from models.predict import LoanApplication
from pydantic import BaseModel

person_collection = database["persons"]
loan_collection = database["loans"]
credit_history_collection = database["credit_history"]
loan_financials_collection = database["loan_financials"]

async def create_all_models(data: dict):
    # Create Person
    person_data = {
        "person_age": data["person_age"],
        "person_gender": data["person_gender"],
        "person_education": data["person_education"],
        "person_income": data["person_income"],
        "person_emp_exp": data["person_emp_exp"],
        "person_home_ownership": data["person_home_ownership"]
    }
    person_result = await person_collection.insert_one(person_data)
    person_id = str(person_result.inserted_id)

    # Create Loan
    loan_data = {
        "person_id": person_id,
        "loan_amnt": data["loan_amnt"],
        "loan_intent": data["loan_intent"],
        "loan_status": data["loan_status"]
    }
    loan_result = await loan_collection.insert_one(loan_data)
    loan_id = str(loan_result.inserted_id)

    # Create Credit History
    credit_history_data = {
        "person_id": person_id,
        "credit_score": data["credit_score"],
        "cb_person_cred_hist_length": data["cb_person_cred_hist_length"],
        "previous_loan_defaults_on_file": data["previous_loan_defaults_on_file"]
    }
    await credit_history_collection.insert_one(credit_history_data)

    # Create Loan Financials
    loan_financials_data = {
        "loan_id": loan_id,
        "loan_int_rate": data["loan_int_rate"],
        "loan_percent_income": data["loan_percent_income"]
    }
    await loan_financials_collection.insert_one(loan_financials_data)

    return {"message": "Data saved successfully!", "person_id": person_id, "loan_id": loan_id}

async def get_person(person_id: str):
    try:
        # Get person data
        person = await person_collection.find_one({"_id": ObjectId(person_id)})
        if not person:
            return None
        
        # Convert ObjectId to string for JSON serialization
        person["_id"] = str(person["_id"])
        
        # Get related loan data
        loans = []
        async for loan in loan_collection.find({"person_id": person_id}):
            loan["_id"] = str(loan["_id"])
            
            # Get loan financials for each loan
            loan_financials = await loan_financials_collection.find_one({"loan_id": str(loan["_id"])})
            if loan_financials:
                loan_financials["_id"] = str(loan_financials["_id"])
                loan["financials"] = loan_financials
            
            loans.append(loan)
        
        # Get credit history
        credit_history = await credit_history_collection.find_one({"person_id": person_id})
        if credit_history:
            credit_history["_id"] = str(credit_history["_id"])
        
        # Combine all data
        result = {
            "person": person,
            "loans": loans,
            "credit_history": credit_history
        }
        
        return result
    except Exception as e:
        return {"error": str(e)}

async def update_person(person_id: str, data: dict):
    try:
        # Update person data
        update_data = {}
        if "person_age" in data: update_data["person_age"] = data["person_age"]
        if "person_gender" in data: update_data["person_gender"] = data["person_gender"]
        if "person_education" in data: update_data["person_education"] = data["person_education"]
        if "person_income" in data: update_data["person_income"] = data["person_income"]
        if "person_emp_exp" in data: update_data["person_emp_exp"] = data["person_emp_exp"]
        if "person_home_ownership" in data: update_data["person_home_ownership"] = data["person_home_ownership"]
        
        if update_data:
            result = await person_collection.update_one(
                {"_id": ObjectId(person_id)},
                {"$set": update_data}
            )
            
            if result.matched_count == 0:
                return {"error": "Person not found"}
                
            return {"message": "Person updated successfully", "modified_count": result.modified_count}
        else:
            return {"message": "No data to update"}
            
    except Exception as e:
        return {"error": str(e)}

async def delete_person(person_id: str):
    try:
        # Find all loans associated with the person
        loans = []
        async for loan in loan_collection.find({"person_id": person_id}):
            loans.append(str(loan["_id"]))
        
        # Delete loan financials for each loan
        for loan_id in loans:
            await loan_financials_collection.delete_many({"loan_id": loan_id})
        
        # Delete loans
        loan_delete_result = await loan_collection.delete_many({"person_id": person_id})
        
        # Delete credit history
        credit_history_delete_result = await credit_history_collection.delete_many({"person_id": person_id})
        
        # Delete person
        person_delete_result = await person_collection.delete_one({"_id": ObjectId(person_id)})
        
        if person_delete_result.deleted_count == 0:
            return {"error": "Person not found"}
            
        return {
            "message": "Person and related data deleted successfully",
            "deleted_counts": {
                "person": person_delete_result.deleted_count,
                "loans": loan_delete_result.deleted_count,
                "loan_financials": sum(1 for _ in loans),
                "credit_history": credit_history_delete_result.deleted_count
            }
        }
    except Exception as e:
        return {"error": str(e)}


# Load the model, scaler, and label encoder
model = load_model('/Users/samenergy/Documents/Projects/Databases_P13/Model/loan_approval_model.h5')

with open('/Users/samenergy/Documents/Projects/Databases_P13/Model/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('/Users/samenergy/Documents/Projects/Databases_P13/Model/label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

# Define Pydantic model for input validation
class LoanApplication(BaseModel):
    person_age: int
    person_gender: str
    person_education: str
    person_income: float
    person_emp_exp: float
    person_home_ownership: str
    loan_amnt: float
    loan_intent: str
    loan_int_rate: float
    loan_percent_income: float
    cb_person_cred_hist_length: int
    credit_score: float
    previous_loan_defaults_on_file: int

def predict_loan_status(loan: LoanApplication):
    # Convert input data into a list
    input_data = [
        loan.person_age,
        loan.person_gender,
        loan.person_education,
        loan.person_income,
        loan.person_emp_exp,
        loan.person_home_ownership,
        loan.loan_amnt,
        loan.loan_intent,
        loan.loan_int_rate,
        loan.loan_percent_income,
        loan.cb_person_cred_hist_length,
        loan.credit_score,
        loan.previous_loan_defaults_on_file
    ]
    
    # Encode categorical variables
    encoded_data = []
    for feature in input_data:
        if isinstance(feature, str):
            if feature in label_encoder.classes_:
                encoded_data.append(label_encoder.transform([feature])[0])
            else:
                encoded_data.append(label_encoder.transform([label_encoder.classes_[0]])[0])  
        else:
            encoded_data.append(feature)
    
    # Convert to numpy array and scale
    input_data = np.array(encoded_data).reshape(1, -1)
    input_data = scaler.transform(input_data)

    # Predict the loan status
    prediction = model.predict(input_data)
    result = "Loan Approved" if prediction[0] > 0.5 else "Loan Rejected"

    # Store in MongoDB
    loan_data = loan.dict()
    loan_data["loan_status"] = result
    collection.insert_one(loan_data)  # Insert into MongoDB collection

    return {"loan_status": result}