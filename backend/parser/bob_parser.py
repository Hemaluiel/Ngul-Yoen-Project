import pdfplumber
import re

def clean_amount(val):
    if not val:
        return 0
    try:
        return float(str(val).replace(",", "").strip())
    except:
        return 0


def parse_bob(file):

    data = []

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            table = page.extract_table()

            # TABLE PARSING IMPROVED
            if table:

                for row in table[1:]:  # skip header

                    if not row or len(row) < 5:
                        continue

                    try:
                        print("ROW:", row)  # DEBUG

                        date = row[0]

                        # Merge description safely - handles shifting columns
                        description = " ".join(
                            [str(x) for x in row[1:-3] if x]
                        ).strip()

                        # Always take last columns for amounts
                        debit = row[-3]
                        credit = row[-2]

                        debit_val = clean_amount(debit)
                        credit_val = clean_amount(credit)

                        if debit_val == 0 and credit_val == 0:
                            continue

                        amount = debit_val if debit_val > 0 else credit_val

                        data.append({
                            "date": date,
                            "description": description,
                            "amount": amount
                        })

                    except Exception as e:
                        print("TABLE ERROR:", row, e)
                        continue

            # TEXT FALLBACK - IMPROVED
            else:
                text = page.extract_text()

                if not text:
                    continue

                lines = text.split("\n")

                for line in lines:

                    # Match date
                    if not re.match(r"\d{2}/\d{2}/\d{4}", line):
                        continue

                    # Extract all numbers
                    nums = re.findall(r"\d{1,3}(?:,\d{3})*\.\d{2}", line)

                    if len(nums) < 2:
                        continue

                    try:
                        debit_val = clean_amount(nums[0])
                        credit_val = clean_amount(nums[1])

                        if debit_val == 0 and credit_val == 0:
                            continue

                        # Clean description
                        desc = re.sub(r"\d{1,3}(?:,\d{3})*\.\d{2}", "", line)
                        desc = desc.replace(line[:10], "").strip()

                        amount = debit_val if debit_val > 0 else credit_val

                        data.append({
                            "date": line[:10],
                            "description": desc,
                            "amount": amount
                        })

                    except Exception as e:
                        print("TEXT ERROR:", line, e)
                        continue

    print("TOTAL PARSED:", len(data))
    return data