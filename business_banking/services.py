LOAN_RULES = {
    "home_loan": {
        "min_salary": 30000,
        "min_age": 25,
        "max_age": 65,
        "account_types": ["Savings", "Current"],
        "max_loan_multiplier": 10  # e.g., max loan = salary * 10
    },
    "business_loan": {
        "min_salary": 50000,
        "min_age": 30,
        "max_age": 70,
        "account_types": ["Current"],
        "max_loan_multiplier": 15
    },
    "education_loan": {
        "min_salary": 15000,
        "min_age": 18,
        "max_age": 35,
        "account_types": ["Savings"],
        "max_loan_multiplier": 5
    }
}


def check_loan_eligibility(user, loan_type):
    rules = LOAN_RULES[loan_type]

    # Extract user data, assuming user is a dict or sqlite3.Row
    print(user["Salary"])
    salary = float(user["Salary"])
    age = 34
    account_type = user["AccountType"]
    pan = user["PAN"]
    tan = user["TAN"]

    # Check PAN/TAN based on account type
    if account_type.lower() == "savings" and not pan:
        return {"status": "fail", "message": "Please update your PAN to proceed with loan application."}
    if account_type.lower() == "current" and not tan:
        return {"status": "fail", "message": "Please update your TAN to proceed with loan application."}

    # Validate loan-specific criteria
    if salary < rules["min_salary"]:
        return {"status": "fail", "message": f"Minimum salary for {loan_type} is {rules['min_salary']}"}

    if age < rules["min_age"] or age > rules["max_age"]:
        return {"status": "fail", "message": f"Age must be between {rules['min_age']} and {rules['max_age']} for {loan_type}"}

    if account_type not in rules["account_types"]:
        return {"status": "fail", "message": f"Loan type '{loan_type}' not available for {account_type} account"}

    # If all checks pass, approve loan
    approved_loan_amount = salary * rules["max_loan_multiplier"]

    return {
        "status": "success",
        "message": f"{loan_type.replace('_', ' ').title()} approved",
        "UserName": user["UserName"],
        "AccountType": account_type,
        "Balance": salary,
        "ApprovedLoanAmount": approved_loan_amount,
        "PAN": pan,
        "TAN": tan
    }

