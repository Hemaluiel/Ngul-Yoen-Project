import re
from difflib import get_close_matches

CATEGORY_RULES = {
    "Food": ["restaurant", "cafe", "hotel", "food", "pizza", "burger"],
    "Shopping": ["shop", "store", "mart", "purchase", "shopping"],
    "Transport": ["fuel", "taxi", "bus", "uber", "petrol"],
    "Bills": ["electricity", "water", "bill", "payment", "fee"],
    "Transfer": ["transfer", "sent", "received", "account"],
    "Entertainment": ["movie", "netflix", "game"],
}


def smart_match(desc):
    desc = desc.lower()

    for category, words in CATEGORY_RULES.items():
        matches = get_close_matches(desc, words, n=1, cutoff=0.6)
        if matches:
            return category

    return None


def categorize(transactions):

    categorized = {}

    for t in transactions:

        desc = t.get("description", "").lower()
        desc = re.sub(r'[^a-zA-Z ]', ' ', desc)
        amount = t.get("amount", 0)

        assigned = None

        # 1. KEYWORD MATCH
        for category, keywords in CATEGORY_RULES.items():
            if any(word in desc for word in keywords):
                assigned = category
                break

        # 2. FUZZY MATCH
        if not assigned:
            assigned = smart_match(desc)

        # 3. DEFAULT
        if not assigned:
            assigned = "Others"

        categorized[assigned] = categorized.get(assigned, 0) + amount

    return categorized