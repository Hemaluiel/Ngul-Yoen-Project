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

                # detect transaction line
                if not re.search(r"\d{2}/\d{2}/\d{4}", line):
                    continue

                nums = re.findall(r"\d{1,3}(?:,\d{3})*\.\d{2}", line)

                if len(nums) < 2:
                    continue

                try:
                    debit = float(nums[0].replace(",", ""))
                    credit = float(nums[1].replace(",", ""))

                    amount = debit if debit > 0 else credit

                    if amount == 0:
                        continue

                    data.append({
                        "date": line[:10],
                        "description": line,
                        "amount": amount
                    })

                except:
                    continue

    print("TOTAL PARSED:", len(data))
    return data