from difflib import get_close_matches

CATEGORY_MAP = {
    "Food": ["restaurant", "cafe", "pizza", "food", "kfc", "burger"],
    "Transport": ["taxi", "uber", "fuel", "petrol", "bus"],
    "Bills": ["electricity", "water", "internet", "bill"],
    "Shopping": ["shop", "store", "mall", "mart"],
    "Transfer": ["transfer", "sent", "received"],
}


def categorize(transactions):

    result = {}

    for t in transactions:

        desc = t["description"].lower()

        category = "Others"

        for cat, keywords in CATEGORY_MAP.items():

            match = get_close_matches(desc, keywords, cutoff=0.6)

            if match:
                category = cat
                break

        result[category] = result.get(category, 0) + t["amount"]

    return result