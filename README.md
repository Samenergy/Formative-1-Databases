# **Formative 1: Databases**  
### **Database Design, Implementation & API Integration**  

## **Overview**  
This project focuses on database design, implementation, and API integration using **SQL (MySQL/PostgreSQL/SQLite)** and **NoSQL (MongoDB)**. It also includes the development of **FastAPI** endpoints for CRUD operations and a script to fetch data for machine learning predictions.

## **Project Tasks**  

### **1. Database Design & Implementation**  
- **SQL Database**: Implemented a relational database with **at least three tables**, defining **primary and foreign keys** for proper relationships.  
- **Stored Procedure & Trigger**: Automated tasks such as **data validation and logging changes**.  
- **ERD Diagram**: Designed a well-structured **Entity Relationship Diagram (ERD)** to visualize the database schema.  
- **MongoDB**: Implemented **collections** for handling NoSQL data.  

### **2. API Development (FastAPI)**  
Implemented CRUD API endpoints for the **relational database**:  
- **POST** → Create new data  
- **GET** → Read data  
- **PUT** → Update data  
- **DELETE** → Delete data  

### **3. Fetch & Predict Script**  
- **Fetch latest entry** via API.  
- **Prepare data for prediction** using a pre-trained machine learning model.  
- **Make predictions** based on the processed data.  

## **Technology Stack**  
- **Database**: MySQL/PostgreSQL/SQLite & MongoDB  
- **Backend**: FastAPI  
- **Machine Learning**: Python (for data prediction script)  
- **Version Control**: Git & GitHub  

## **Installation & Setup**  
1. **Clone the Repository**  
   ```bash
   git clone https://github.com/your-repo-url.git
   cd your-repo-folder
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
   Open in your browser:  
   ```
   http://127.0.0.1:8000/docs
   ```

## **Contributors**  
- **[Team Member 1]** - MongoDB Implementation  
- **[Team Member 2]** - API Development  
- **[Team Member 3]** - Fetch & Prediction  
