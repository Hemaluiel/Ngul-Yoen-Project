from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from core.detect_bank import detect_bank
from utils.pdf_reader import extract_text
from parser.bank_router import route_parser
from core.dedupe import dedupe
from utils.categorizer import categorize

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    print("FILE RECEIVED:", file.filename)

    # STEP 1: detect bank
    text = extract_text(file)
    bank = detect_bank(text)
    print("BANK:", bank)

    # IMPORTANT: reset file pointer
    file.seek(0)

    # STEP 2: parse transactions
    raw = route_parser(bank, file)
    print("RAW COUNT:", len(raw))

    # STEP 3: remove duplicates
    clean = dedupe(raw)
    print("CLEAN COUNT:", len(clean))

    # STEP 4: categorize
    categorized = categorize(clean)

    return jsonify({
        "bank": bank,
        "transactions": clean,
        "categories": categorized
    })


if __name__ == "__main__":
    app.run(debug=True)