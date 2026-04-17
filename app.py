from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Server is running ✅"

# Simple categorization rules
def categorize(text):
    categories = {
        "Food": ["restaurant", "cafe", "zomato", "drinks", "water", "juice"],
        "Transport": ["taxi", "fuel", "bus", "train", "car", "taxifare", "travel", "transport"],
        "Shopping": ["store", "mall", "amazon", "grocery", "supermarket", "clothing", "electronics", "shopping", "groceries", "vegetables", "fruits"],
        "Bills and utilities": ["electricity", "waterbill", "internet", "recharge", "rent", "utilities", "bill", "subscription", "999", "777", "gas"],
        "Entertainment": ["movie", "netflix", "spotify", "concert", "entertainment", "game", "gaming", "theater", "music"],
        "Health": ["pharmacy", "doctor", "hospital", "medicine", "health", "fitness", "gym"],
        "Education": ["book", "course", "education", "school", "university", "tuition", "onlinecourse", "learning", "coursefee", "oen and pencil", "stationery"],
        "Others": []
    }

    result = {key: 0 for key in categories}
    result["Others"] = 0

    lines = text.split("\n")

    for line in lines:
        for category, keywords in categories.items():
            if any(word in line.lower() for word in keywords):
                result[category] += 100  # simulate amount

    return result


@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files["file"]

    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    data = categorize(text)

    total = sum(data.values())

    response = {
        "categories": data,
        "total": total
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
