import pdfplumber
import re

def clean_amount(x):
    if not x:
        return 0
    x = str(x).replace(",", "").replace("H", "").strip()
    try:
        return float(x)
    except:
        return 0


def parse_bob(file):

    data = []

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            text = page.extract_text()
            if not text:
                continue

            lines = text.split("\n")

            for i, line in enumerate(lines):

                # ✅ detect transaction line by DATE
                if not re.match(r"\d{2}/\d{2}/\d{4}", line):
                    continue

                try:
                    parts = line.split()

                    date = parts[0]

                    # extract numbers (debit, credit, balance)
                    nums = re.findall(r"\d{1,3}(?:,\d{3})*\.\d{2}", line)

                    if len(nums) < 2:
                        continue

                    debit = clean_amount(nums[0])
                    credit = clean_amount(nums[1])

                    amount = debit if debit > 0 else credit

                    # 🔥 extract description
                    desc = line.replace(date, "")

                    for num in nums:
                        desc = desc.replace(num, "")

                    desc = desc.strip()

                    # ✅ if description too short → take next line
                    if len(desc) < 3 and i + 1 < len(lines):
                        desc = lines[i + 1].strip()

                    # ❌ skip empty rows
                    if amount == 0:
                        continue

                    data.append({
                        "date": date,
                        "description": desc,
                        "amount": amount
                    })

                except Exception as e:
                    print("PARSE ERROR:", e)
                    continue

    print("TOTAL PARSED:", len(data))

    return data