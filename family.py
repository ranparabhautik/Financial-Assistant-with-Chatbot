# family.py

import json
import os

DATA_FILE = "finance_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"income": 0, "savings": 0, "expenses": {}, "logs": [], "family": []}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_family_member(name, age, relation, is_earning):
    data = load_data()
    if "family" not in data:
        data["family"] = []

    member = {
        "name": name,
        "age": age,
        "relation": relation,
        "is_earning": is_earning
    }

    data["family"].append(member)
    save_data(data)
    return f"✅ Added {relation} '{name}' to family profile."

def get_family_members():
    data = load_data()
    return data.get("family", [])
