from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Server is running for Ngul~Yoen PDF Analysis"


def categorize_transactions(rows):
    categories = {
        "Food": ["restaurant", "cafe", "zomato", "drinks", "water", "juice", "food", "meal", "dining", "snack", "coffee", "tea", "fastfood", "dinner", "lunch", "breakfast", "momo", "Maggie", "rice"],
        "Transport": ["taxi", "fuel", "bus", "train", "car", "taxifare", "travel", "transport"],
        "Shopping": ["store", "mall", "amazon", "grocery", "supermarket", "clothing", "electronics", "shopping", "groceries", "vegetables", "fruits"],
        "Bills and utilities": ["electricity", "waterbill", "internet", "recharge", "rent", "utilities", "ebill", "subscription", "999", "777", "gas", "BT Recharge"],
        "Entertainment": ["movie", "netflix", "spotify", "concert", "entertainment", "game", "gaming", "theater", "music"],
        "Health": ["pharmacy", "doctor", "hospital", "medicine", "health"],
        "Personal Care": ["fitness", "gym", "salon", "spa", "personalcare", "cream", "shampoo", "skincare", "haircut", "barber", "cosmetics"],
        "Education": ["book", "course", "education", "school", "university", "tuition", "onlinecourse", "learning", "coursefee", "oen and pencil", "stationery"],
        "Others": []
    }

    result = {key: 0 for key in categories}

    for row in rows:
        try:
            # based on table structure: [date, particulars, journal, ref, debit, credit, balance]

            particulars = row[1] if row[1] else ""
            debit = row[4]

            if not debit:
                continue

            debit = float(debit)

            # Only debit transactions
            if debit > 0:
                text = particulars.lower()

                matched = False
                for category, keywords in categories.items():
                    if any(word in text for word in keywords):
                        result[category] += debit
                        matched = True
                        break

                if not matched:
                    result["Others"] += debit

        except:
            continue

    return result


@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files["file"]

    all_rows = []

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            table = page.extract_table()

            if table:
                # Skipping header row
                for row in table[1:]:
                    all_rows.append(row)

    data = categorize_transactions(all_rows)
    total = sum(data.values())

    return jsonify({
        "categories": data,
        "total": total
    })


if __name__ == "__main__":
    app.run(debug=True)

