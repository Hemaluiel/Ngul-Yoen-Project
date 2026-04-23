def categorize(data):
    for tx in data:
        desc = tx["description"].lower()

        if "fuel" in desc:
            tx["category"] = "Transport"
        elif "restaurant" in desc or "hotel" in desc:
            tx["category"] = "Food"
        elif "transfer" in desc:
            tx["category"] = "Transfer"
        else:
            tx["category"] = "Others"

    return data