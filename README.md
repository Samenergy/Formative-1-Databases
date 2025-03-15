# **Formative 1: Databases**  
### **Loan Management System with SQL, MongoDB, and ML Integration**  

## **Overview**  
This project implements a comprehensive loan management system with both SQL (MySQL) and NoSQL (MongoDB) databases. It features FastAPI endpoints for CRUD operations and integrates a machine learning model for loan approval predictions based on applicant data.

## **Project Structure**  
```
├── MySQL/              # SQL implementation
│   ├── config/         # Database configuration
│   ├── controllers/    # Logic for database operations
│   ├── models/         # Database models
│   ├── routes/         # API endpoints
│   ├── main.py         # FastAPI application
│   ├── requirements.txt # Dependencies
│   ├── ERD.png         # Entity Relationship Diagram
│   └── schema.sql      # Database schema definition
│
├── MongoDB/            # NoSQL implementation
│   ├── config/         # MongoDB configuration
│   ├── controllers/    # Logic for database operations
│   ├── models/         # MongoDB schemas
│   ├── routes/         # API endpoints
│   ├── main.py         # FastAPI application
│   └── requirements.txt # Dependencies
│
└── Model/              # Machine Learning components
    ├── loan_approval_model.keras  # Trained ML model
    ├── best_loan_approval_model.keras # Best model version
    ├── label_encoder.pkl # Label encoder for categorical data
    ├── scaler.pkl     # Data scaler for normalization
    └── Notebook.ipynb # ML model development notebook
```

## **Features**  

### **1. MySQL Database**  
- **Schema Design**: Relational database with 4 tables:
  - Person (personal details)
  - Loan (loan information)
  - Credit_History (credit score and history)
  - Loan_Financials (interest rates and financial details)
- **Relationships**: Defined primary and foreign keys ensuring data integrity
- **ERD Diagram**: Visual representation of database relationships

### **2. MongoDB Database**  
- **NoSQL Implementation**: Document-based storage for loan management data
- **Collections**: Structured for efficient NoSQL operations

### **3. API Endpoints (FastAPI)**  
- **MySQL API**:
  - CRUD operations for all database entities
  - Data validation
  - Error handling
  
- **MongoDB API**:
  - CRUD operations optimized for document-based storage
  - Integration with ML prediction

### **4. Machine Learning Integration**  
- **Loan Approval Model**: Neural network trained on historical loan data
- **Features**: Uses applicant demographics, loan details, and credit history
- **Prediction**: Returns loan approval probability based on input data
- **Supporting Tools**: Label encoder and scaler for data preparation

## **Technology Stack**  
- **Databases**: MySQL (Relational) & MongoDB (NoSQL)
- **API Framework**: FastAPI
- **Machine Learning**: TensorFlow/Keras, Scikit-learn
- **Programming Language**: Python 3
- **Version Control**: Git & GitHub

## **Installation & Setup**  

### **MySQL Application**
1. **Navigate to MySQL directory**
   ```bash
   cd MySQL
   ```
2. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up the database**
   ```bash
   # Import schema.sql to your MySQL server
   ```
4. **Run the FastAPI Server**  
   ```bash
   uvicorn main:app --reload
   ```
5. **Access API Documentation**  
   ```
   http://127.0.0.1:8000/docs
   ```

### **MongoDB Application**
1. **Navigate to MongoDB directory**
   ```bash
   cd MongoDB
   ```
2. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the FastAPI Server**  
   ```bash
   uvicorn main:app --reload
   ```
4. **Access API Documentation**  
   ```
   http://127.0.0.1:8000/docs
   ```

## **Contributors**  
- **Samuel Dushime**
- **Juliana Crystal Holder**
- **Jules Gatete** 

## **Dataset**
The project uses a loan dataset (loan_data.csv) with applicant details, loan information, and approval status for training the machine learning model.
Source: [Kaggle - Loan Approval Classification Dataset](https://www.kaggle.com/datasets/taweilo/loan-approval-classification-data?resource=download)
