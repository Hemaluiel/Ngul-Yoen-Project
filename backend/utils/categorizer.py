def categorize(data):
    categories = {
        "Food": ["restaurant", "cafe", "zomato", "drinks", "water", "juice", "food", "meal", "dining",
                 "snack", "coffee", "tea", "fastfood", "dinner", "lunch", "breakfast", "momo", "maggie", "rice"],

        "Transport": ["taxi", "fuel", "bus", "train", "car", "taxifare", "travel", "transport"],

        "Shopping": ["store", "mall", "amazon", "grocery", "supermarket", "clothing", "electronics",
                     "shopping", "groceries", "vegetables", "fruits", "shoes", "accessories", "shop", "shopp"],

        "Bills and utilities": ["electricity", "waterbill", "internet", "recharge", "rent", "utilities",
                                "ebill", "subscription", "999", "777", "gas", "bt recharge"],

        "Entertainment": ["movie", "netflix", "spotify", "concert", "entertainment", "game",
                          "gaming", "theater", "music"],

        "Health": ["pharmacy", "doctor", "hospital", "medicine", "health"],

        "Personal Care": ["fitness", "gym", "salon", "spa", "personalcare", "cream",
                          "shampoo", "skincare", "haircut"],

        "Others": []
    }

    for tx in data:
        desc = (tx.get("description") or "").lower()
        assigned = False

        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in desc:
                    tx["category"] = category
                    assigned = True
                    break
            if assigned:
                break

        if not assigned:
            tx["category"] = "Others"

    return data