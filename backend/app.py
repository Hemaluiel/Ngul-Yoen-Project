from flask import Flask, request, jsonify
from parser.detect_bank import detect_bank
from parser.bob_parser import parse_bob
from parser.bnb_parser import parse_bnb
from parser.generic_parser import parse_generic
from utils.pdf_reader import extract_text
from utils.categorizer import categorize

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload_pdf():
    file = request.files["file"]

    # Step 1: extract text
    text = extract_text(file)

    # Step 2: detect bank
    bank = detect_bank(text)
    print("Detected Bank:", bank)

    # Step 3: route parser
    file.seek(0)  # reset file pointer

    if bank == "BOB":
        data = parse_bob(file)
    elif bank == "BNB":
        data = parse_bnb(file)
    else:
        data = parse_generic(text)

    # Step 4: categorize
    result = categorize(data)

    return jsonify({
        "bank": bank,
        "transactions": result
    })

if __name__ == "__main__":
    app.run(debug=True)