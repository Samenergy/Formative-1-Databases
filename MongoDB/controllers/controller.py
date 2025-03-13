from config.db import database
from bson import ObjectId

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

