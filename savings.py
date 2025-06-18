def calculate_savings(income, expenses):
    return income - sum(expenses)

def project_future_savings(current_savings, months, monthly_save):
    return current_savings + months * monthly_save
