-- Create the database (optional)
CREATE DATABASE LoanManagementDB;
USE LoanManagementDB;

-- Table: Person (Stores personal details)
CREATE TABLE Person (
    person_id INT AUTO_INCREMENT PRIMARY KEY,
    age INT NOT NULL,
    gender ENUM('male', 'female') NOT NULL,
    education ENUM('High School', 'Bachelor', 'Master') NOT NULL,
    income DECIMAL(10,2) NOT NULL,
    emp_exp INT NOT NULL,
    home_ownership ENUM('RENT', 'OWN', 'MORTGAGE') NOT NULL
);

-- Table: Loan (Stores loan details)
CREATE TABLE Loan (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,
    person_id INT NOT NULL,
    loan_amount DECIMAL(10,2) NOT NULL,
    loan_intent ENUM('PERSONAL', 'EDUCATION', 'MEDICAL', 'VENTURE') NOT NULL,
    loan_status BOOLEAN NOT NULL, -- 1 = Approved, 0 = Rejected
    FOREIGN KEY (person_id) REFERENCES Person(person_id) ON DELETE CASCADE
);

-- Table: Credit_History (Stores credit history details)
CREATE TABLE Credit_History (
    credit_id INT AUTO_INCREMENT PRIMARY KEY,
    person_id INT NOT NULL,
    credit_score INT NOT NULL CHECK (credit_score BETWEEN 300 AND 850),
    cred_hist_length INT NOT NULL,
    previous_defaults ENUM('Yes', 'No') NOT NULL,
    FOREIGN KEY (person_id) REFERENCES Person(person_id) ON DELETE CASCADE
);

-- Table: Loan_Financials (Stores loan interest and financial details)
CREATE TABLE Loan_Financials (
    finance_id INT AUTO_INCREMENT PRIMARY KEY,
    loan_id INT NOT NULL,
    interest_rate DECIMAL(5,2) NOT NULL,
    percent_income DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (loan_id) REFERENCES Loan(loan_id) ON DELETE CASCADE
);
