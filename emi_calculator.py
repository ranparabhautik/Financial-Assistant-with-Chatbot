def calculate_emi(principal, rate, months):
    r = rate / (12 * 100)
    emi = principal * r * ((1 + r)**months) / ((1 + r)**months - 1)
    return round(emi, 2)

def savings_goal_plan(goal_amount, current_savings, months):
    need_to_save = goal_amount - current_savings
    per_month = need_to_save / months if months > 0 else 0
    return round(per_month, 2)
