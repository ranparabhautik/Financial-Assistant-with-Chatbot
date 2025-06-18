import re

def extract_intent_entities(user_input):
    user_input = user_input.lower()

    # INTENTS
    if "add expense" in user_input:
        intent = "add_expense"
        match = re.search(r'(\d+).*for\s+(\w+)', user_input)
        if match:
            amount = int(match.group(1))
            category = match.group(2).capitalize()
            return intent, {"amount": amount, "category": category}
        return intent, {}

    elif "how much did i spend" in user_input:
        intent = "category_query"
        match = re.search(r'spend on (\w+)', user_input)
        if match:
            category = match.group(1).capitalize()
            return intent, {"category": category}
        return intent, {}

    elif "spending analysis" in user_input or "where i spend" in user_input:
        return "spending_analysis", {}

    elif "savings" in user_input:
        return "savings_check", {}

    elif "suggest" in user_input or "advice" in user_input:
        return "suggestion", {}

    return "unknown", {}
