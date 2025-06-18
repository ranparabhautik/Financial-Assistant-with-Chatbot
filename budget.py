def check_budget_status(income, expenses, budget):
    total_expense = sum(expenses)
    return "Under Budget" if total_expense <= budget else "Over Budget"

def optimize_budget_allocation(income, expenses):
    # DAA: Greedy method to keep highest remaining
    sorted_exp = sorted(expenses)
    allocated = 0
    for e in sorted_exp:
        if allocated + e > income:
            break
        allocated += e
    return allocated, income - allocated
