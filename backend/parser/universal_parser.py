import pdfplumber
import re

from parser.ocr_parser import ocr_parse_pdf  # optional later

DATE_PATTERN = r"\d{2}/\d{2}/\d{4}"
AMOUNT_PATTERN = r"\d{1,3}(?:,\d{3})*\.\d{2}"


def clean_amount(x):
    try:
        return float(x.replace(",", ""))
    except:
        return 0


def extract_transactions_from_text(text):

    transactions = []
    lines = text.split("\n")

    for line in lines:

        if not re.search(DATE_PATTERN, line):
            continue

        amounts = re.findall(AMOUNT_PATTERN, line)

        if len(amounts) < 2:
            continue

        debit = clean_amount(amounts[0])
        credit = clean_amount(amounts[1])

        amount = debit if debit > 0 else credit

        desc = re.sub(AMOUNT_PATTERN, "", line)
        desc = re.sub(DATE_PATTERN, "", desc).strip()

        if amount == 0:
            continue

        transactions.append({
            "date": line[:10],
            "description": desc,
            "amount": amount
        })

    return transactions


def parse_with_pdfplumber(file):

    data = []

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:

            text = page.extract_text()

            if text:
                data.extend(extract_transactions_from_text(text))

            # fallback table extraction
            table = page.extract_table()
            if table:
                for row in table:
                    if not row:
                        continue

    return data


def parse_universal(file):

    # 1 try pdf text parsing
    data = parse_with_pdfplumber(file)

    if len(data) > 0:
        return data

    # 2 fallback OCR (future)
    try:
        data = ocr_parse_pdf(file)
        if len(data) > 0:
            return data
    except:
        pass

    return []