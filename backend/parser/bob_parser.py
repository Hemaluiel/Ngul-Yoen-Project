import pdfplumber
import re

def parse_bob(file):

    data = []

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:

            text = page.extract_text()

            if not text:
                continue

            lines = text.split("\n")

            for line in lines:

                print("LINE:", line)  # 🔍 DEBUG

                # must contain date
                if not re.search(r"\d{2}/\d{2}/\d{4}", line):
                    continue

                # extract numbers
                nums = re.findall(r"\d{1,3}(?:,\d{3})*\.\d{2}", line)

                # 🔥 FIX: accept even ONE number
                if len(nums) == 0:
                    continue

                try:
                    # take LAST number as amount (most reliable)
                    amount = float(nums[-1].replace(",", ""))

                    # skip tiny balances (optional)
                    if amount == 0:
                        continue

                    data.append({
                        "date": line[:10],
                        "description": line,
                        "amount": amount
                    })

                except Exception as e:
                    print("ERROR:", e)
                    continue

    print("TOTAL PARSED:", len(data))
    return data