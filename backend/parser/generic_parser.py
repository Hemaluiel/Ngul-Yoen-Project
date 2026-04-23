import re

def parse_generic(text):
    data = []

    lines = text.split("\n")

    for line in lines:
        # simple pattern: date + description + amount
        match = re.search(r'(\d{2}/\d{2}/\d{4}).*?(-?\d+\.\d+)', line)

        if match:
            date = match.group(1)
            amount = float(match.group(2))

            if amount < 0:  # treat negative as debit
                data.append({
                    "date": date,
                    "description": line,
                    "amount": abs(amount),
                    "type": "debit"
                })

    return data