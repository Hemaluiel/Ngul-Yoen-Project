import pdfplumber
import re

def parse_bob(file):

    data = []
    seen = set()

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            text = page.extract_text()
            if not text:
                continue

            lines = text.split("\n")

            for line in lines:

                # must start with date
                if not re.match(r"\d{2}/\d{2}/\d{4}", line):
                    continue

                try:
                    amounts = re.findall(r"\d{1,3}(?:,\d{3})*\.\d{2}", line)

                    if len(amounts) < 2:
                        continue

                    debit = float(amounts[0].replace(",", ""))
                    credit = float(amounts[1].replace(",", ""))

                    # Fix: only take debit (expense)
                    if debit <= 0:
                        continue

                    amount = debit

                    # extract description FIRST
                    desc = re.sub(r"\d{1,3}(?:,\d{3})*\.\d{2}", "", line)
                    desc = re.sub(r"\d{2}/\d{2}/\d{4}", "", desc)
                    desc = re.sub(r"[^a-zA-Z ]", " ", desc)
                    desc = re.sub(r"\s+", " ", desc).strip()

                    if not desc:
                        continue

                    # remove duplicates safely
                    key = f"{line[:10]}-{amount}-{desc}"
                    if key in seen:
                        continue
                    seen.add(key)

                    data.append({
                        "date": line[:10],
                        "description": desc,
                        "amount": amount
                    })

                except Exception as e:
                    print("PARSE ERROR:", e)
                    continue

    print("TOTAL PARSED:", len(data))
    return data