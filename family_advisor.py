from datetime import datetime
import json

def suggest_family_budget_plan(data):
    """
    Suggest a family budget plan based on income and expenses.
    
    Args:
        data (dict): Dictionary containing financial data
        
    Returns:
        dict: Budget recommendations with income/expense analysis
    """
    income = data.get("income", 0)
    spouse_income = data.get("family_profile", {}).get("spouse_income", 0)
    total_income = income + spouse_income
    total_expense = sum(sum(v) for v in data.get("expenses", {}).values())

    recommended_saving = round(total_income * 0.20)
    recommended_needs = round(total_income * 0.50)
    recommended_wants = round(total_income * 0.30)

    advice = {
        "total_income": total_income,
        "total_expense": total_expense,
        "current_savings_rate": f"{round((total_income - total_expense)/total_income*100)}%" 
                               if total_income > 0 else "0%",
        "recommended_budget": {
            "needs (50%)": recommended_needs,
            "wants (30%)": recommended_wants,
            "savings (20%)": recommended_saving,
        },
        "budget_status": "Within recommended limits" 
                       if total_expense <= (recommended_needs + recommended_wants) 
                       else "Over budget"
    }

    return advice

def suggest_child_education_plan(data):
    """
    Generate education savings plan for children based on their current ages.
    
    Args:
        data (dict): Dictionary containing family profile data
        
    Returns:
        list: List of personalized education savings recommendations for each child
    """
    children = data.get("family_profile", {}).get("children", [])
    advice = []
    
    for i, age in enumerate(children, start=1):
        years_left = max(18 - age, 0)
        
        # Base education fund target (₹5 lakhs)
        target_fund = 500000  
        
        # Adjust target based on inflation (3% per year)
        inflated_target = round(target_fund * (1.03 ** years_left))
        
        if years_left > 0:
            monthly_saving = round(inflated_target / (years_left * 12))
            
            advice.append(
                f"👶 Child {i} (Age {age}): "
                f"Save ₹{monthly_saving:,}/month "
                f"(₹{inflated_target:,} target in {years_left} years)"
            )
        else:
            advice.append(
                f"👶 Child {i} (Age {age}): "
                "Already at or past college age. "
                "Consider continuing education or vocational training funds."
            )
    
    if not advice:
        advice.append("ℹ️ No children in family profile for education planning")
    
    return advice

def suggest_emergency_fund_plan(data):
    """
    Calculate recommended emergency fund based on monthly expenses.
    
    Args:
        data (dict): Dictionary containing financial data
        
    Returns:
        str: Formatted emergency fund recommendation
    """
    monthly_expense = sum(sum(v) for v in data.get("expenses", {}).values())
    emergency_fund_goal = monthly_expense * 6
    current_savings = data.get("savings", 0)
    
    if current_savings >= emergency_fund_goal:
        return f"✅ Emergency Fund: ₹{current_savings:,} (Fully funded! Goal: ₹{emergency_fund_goal:,})"
    else:
        shortfall = emergency_fund_goal - current_savings
        return (
            f"💼 Recommended Emergency Fund: ₹{emergency_fund_goal:,} (6x monthly expenses)\n"
            f"Current savings: ₹{current_savings:,}\n"
            f"Additional ₹{shortfall:,} needed to reach goal"
        )

def suggest_spouse_retirement_plan(data):
    """
    Generate retirement savings advice for spouse if applicable.
    
    Args:
        data (dict): Dictionary containing family profile data
        
    Returns:
        str or None: Retirement advice if applicable, else None
    """
    family_profile = data.get("family_profile", {})
    married = family_profile.get("married", False)
    spouse_income = family_profile.get("spouse_income", 0)
    
    if not married:
        return None
        
    if spouse_income > 0:
        monthly_contribution = round(spouse_income * 0.15)
        annual_contribution = monthly_contribution * 12
        return (
            f"👩 Spouse Retirement Plan:\n"
            f"- Save ₹{monthly_contribution:,}/month (~15% of income)\n"
            f"- ₹{annual_contribution:,}/year towards retirement\n"
            f"- Consider NPS or PPF for tax benefits"
        )
    else:
        return (
            "👩 Spouse Retirement Considerations:\n"
            "- Spouse has no income\n"
            "- Consider joint retirement planning\n"
            "- Explore voluntary PF contributions"
        )

def generate_family_advice_summary(data):
    """
    Generate comprehensive family financial advice summary.
    
    Args:
        data (dict): Dictionary containing all financial data
        
    Returns:
        dict: Structured financial advice across multiple categories
    """
    summary = {
        "📊 Budget Advice": suggest_family_budget_plan(data),
        "🎓 Child Education": suggest_child_education_plan(data),
        "💼 Emergency Fund": suggest_emergency_fund_plan(data),
    }
    
    retirement_advice = suggest_spouse_retirement_plan(data)
    if retirement_advice:
        summary["👵 Spouse Retirement"] = retirement_advice
    
    # Add timestamp
    summary["🕒 Last Updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return summary

def build_llm_prompt(data):
    """
    Generates a comprehensive prompt string from family data for LLM input.
    
    Args:
        data (dict): Dictionary containing family financial data
        
    Returns:
        str: Well-formatted prompt for LLM financial advice
    """
    family = data.get("family_profile", {})
    
    prompt = f"""
    I'm a financial advisor. Here is the family's profile:
    
    **Monthly Income**: ₹{data.get("income", 0):,}
    **Spouse Income**: ₹{family.get("spouse_income", 0):,}
    **Current Savings**: ₹{data.get("savings", 0):,}
    
    **Family Status**:
    - Married: {"Yes" if family.get("married") else "No"}
    - Children Ages: {", ".join(str(age) for age in family.get("children", [])) or "None"}
    - Dependents: {", ".join(family.get("dependents", [])) or "None"}
    
    **Monthly Expenses**:
    {json.dumps(data.get("expenses", {}), indent=4)}
    
    Please provide a comprehensive financial plan covering:
    1. Budget allocation (50/30/20 rule customization)
    2. Emergency fund strategy (6-12 months calculation)
    3. Child education planning (age-based recommendations)
    4. Spouse retirement planning (if applicable)
    5. Tax-efficient investment suggestions
    6. Insurance needs assessment
    
    Provide the advice in markdown format with clear sections.
    """
    return prompt