from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from parser.detect_bank import detect_bank
from parser.bob_parser import parse_bob
from parser.dk_parser import parse_dk
from parser.bnb_parser import parse_bnb
from parser.generic_parser import parse_generic
from parser.universal_parser import parse_universal
from utils.pdf_reader import extract_text
from utils.categorizer import categorize


app = Flask(__name__)

CORS(app)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_pdf():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    print("FILE RECEIVED:", file.filename)

    text = extract_text(file)

    bank = detect_bank(text)
    print("BANK DETECTED:", bank)

    file.seek(0)

    if bank == "BOB":
        data = parse_bob(file)
    elif bank == "BNB":
        data = parse_bnb(file)
    elif bank == "DK":
        data = parse_dk(file)
    else:
        data = parse_universal(file)

    # 🔥 STOP EARLY IF PARSER FAILS
    if not data or len(data) == 0:
        print("❌ PARSER FAILED - NO TRANSACTIONS FOUND")
        return jsonify({
            "error": "No transactions parsed from PDF",
            "bank": bank
        }), 400

    print("DATA FROM PARSER:", data[:5])
    print("TOTAL TRANSACTIONS:", len(data))

    result = categorize(data)

    print("FINAL RESULT LENGTH:", len(result))

    return jsonify({
        "bank": bank,
        "transactions": result
    })


if __name__ == "__main__":
    app.run(debug=True)