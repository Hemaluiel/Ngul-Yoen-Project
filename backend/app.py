from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from parser.detect_bank import detect_bank
from parser.bob_parser import parse_bob
from parser.dk_parser import parse_dk
from parser.bnb_parser import parse_bnb
from parser.generic_parser import parse_generic
from utils.pdf_reader import extract_text
from utils.categorizer import categorize


app = Flask(__name__)

CORS(app)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_pdf():
    file = request.files["file"]

    # to check if file is received
    print("FILE RECEIVED:", file.filename)

    # Step 1: extract text
    text = extract_text(file)

    # Step 2: detect bank
    bank = detect_bank(text)
    
    # to check detected bank
    print("Detected Bank:", bank) 

    # Step 3: route parser
    file.seek(0)

    if bank == "BOB":
        data = parse_bob(file)
    elif bank == "BNB":
        data = parse_bnb(file)
    elif bank == "DK":
        data = parse_dk(file)
    else:
        data = parse_generic(text)

    # Step 4: categorize
    result = categorize(data)

    # to check the number of transactions parsed
    print("DATA LENGTH:", len(result))

    return jsonify({
        "bank": bank,
        "transactions": result
    })


if __name__ == "__main__":
    app.run(debug=True)