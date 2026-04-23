from difflib import get_close_matches

CATEGORY_MAP = {
    "Food": ["restaurant", "cafe", "zomato", "drinks", "water", "juice", "food", "meal", "dining", "snack", "coffee", "tea", "fastfood", "dinner", "lunch", "breakfast", "momo", "Maggie", "rice"],
    "Transport": ["taxi", "fuel", "bus", "train", "car", "taxifare", "travel", "transport", "uber", "lyft", "cab", "metro", "subway"],
    "Shopping": ["store", "mall", "amazon", "grocery", "supermarket", "clothing", "electronics", "shopping", "groceries", "vegetables", "fruits", "shoes", "accessories", "shop", "shopp"],
    "Bills and utilities": ["electricity", "waterbill", "internet", "recharge", "rent", "utilities", "ebill", "subscription", "999", "777", "gas", "BT Recharge", "wifi", "utility"],
    "Entertainment": ["movie", "netflix", "spotify", "concert", "entertainment", "game", "gaming", "theater", "music"],
    "Health": ["pharmacy", "doctor", "hospital", "medicine", "health"],
    "Transfer": ["transfer", "sent", "bank", "account", "payment", "pay", "withdrawal", "deposit"],
    "Loans": ["loan", "borrow", "lending", "debt", "credit"],
    "Education": ["school", "college", "university", "education", "course", "tuition", "books", "study", "training", "class", "workshop", "seminar", "onlinecourse", "webinar", "educationfee", "examfee", "library", "stationery", "pencil", "notebook", "backpack", "laptop", "software", "edtech"],
    "Support and Donations": ["donation", "charity", "contribution", "fundraiser", "support", "help", "aid", "sponsorship", "SEMSO", "semso", "donate", "donated", "small contribution", "contribution", "volunteer", "volunteering"],
    "Birthdays, Anniversaries, and Celebrations": ["birthday", "bdy", "anniversary", "celebration", "party", "event", "gathering", "festivity", "special occasion", "wedding", "baby shower", "graduation", "holiday", "festival", "ceremony", "birthday gift", "anniversary gift", "celebration gift", "party supplies", "event planning", "gathering expenses", "festivity costs", "special occasion expenses", "milestone celebration", "wedding expenses", "baby shower expenses",("gift list"), ("gift box"), ("gift bag"), ("gift basket")]
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