from transformers import pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def get_intent_hf(user_input):
    intents = ["add_expense", "show_expenses", "savings_check", "suggestion", "goal_planning", "emi_calculation"]
    result = classifier(user_input, candidate_labels=intents)
    return result["labels"][0]
