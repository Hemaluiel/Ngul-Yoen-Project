from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pdfplumber

app = Flask(__name__)
CORS(app)



@app.route("/")
def serve_frontend():
    return send_from_directory(".", "index.html")

@app.route("/status")
def home():
    return "Server is running for Ngul~Yoen PDF Analysis"


def categorize_transactions(rows):
    categories = {
        "Food": ["restaurant", "cafe", "zomato", "drinks", "water", "juice", "food", "meal", "dining", "snack", "coffee", "tea", "fastfood", "dinner", "lunch", "breakfast", "momo", "Maggie", "rice"],
        "Transport": ["taxi", "fuel", "bus", "train", "car", "taxifare", "travel", "transport"],
        "Shopping": ["store", "mall", "amazon", "grocery", "supermarket", "clothing", "electronics", "shopping", "groceries", "vegetables", "fruits", "shoes", "accessories", "shop", "shopp"],
        "Bills and utilities": ["electricity", "waterbill", "internet", "recharge", "rent", "utilities", "ebill", "subscription", "999", "777", "gas", "BT Recharge"],
        "Entertainment": ["movie", "netflix", "spotify", "concert", "entertainment", "game", "gaming", "theater", "music"],
        "Health": ["pharmacy", "doctor", "hospital", "medicine", "health"],
        "Personal Care": ["fitness", "gym", "salon", "spa", "personalcare", "cream", "shampoo", "skincare", "haircut"],
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

    # return jsonify({
    #     "categories": data,
    #     "total": total
    # })

    top5 = extract_top_expenses(all_rows)

    return jsonify({
        "categories": data,
        "total": total,
        "top5": top5
    })

def extract_top_expenses(rows):
    transactions = []

    for row in rows:
        try:
            particulars = row[1]
            debit = row[4]

            if debit and float(debit) > 0:
                transactions.append({
                    "name": particulars,
                    "amount": float(debit)
                })
        except:
            continue

    # Sort descending
    transactions.sort(key=lambda x: x["amount"], reverse=True)

    return transactions[:5]



# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

